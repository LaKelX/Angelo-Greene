"""
VERIFICATION ENGINE
===================
Web-First Empirical Verification Engine for Eudaimon AI

Performs multi-source verification of market data, events, and filings
with confidence scoring based on source agreement and freshness.

Integrates with:
- Lead Quant for local knowledge search
- Lead Inventor for thesis verification
- Web Research Agent for external data
"""

import asyncio
import aiohttp
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json
import hashlib

from .config import config


class DataSource(Enum):
    """Trusted data source categories"""
    MARKET = "market"
    GOVERNMENT = "government"
    OPTIONS = "options"
    NEWS = "news"
    LOCAL = "local"


class VerificationStatus(Enum):
    """Status of verification result"""
    VERIFIED = "verified"          # Multiple sources agree
    PARTIALLY_VERIFIED = "partial" # Some sources agree
    UNVERIFIED = "unverified"      # Single source only
    CONFLICTING = "conflicting"    # Sources disagree
    STALE = "stale"                # Data is outdated
    FAILED = "failed"              # Verification failed


@dataclass
class DataTimestamp:
    """
    Track data freshness and provenance

    Attributes:
        fetched_at: When data was retrieved
        source_timestamp: Original timestamp from source (if available)
        source: Name of the data source
        source_url: URL where data was fetched
        ttl_seconds: Time-to-live before considered stale
    """
    fetched_at: datetime
    source: str
    source_url: str = ""
    source_timestamp: Optional[datetime] = None
    ttl_seconds: int = 300  # 5 minutes default

    @property
    def age_seconds(self) -> float:
        """Get age of data in seconds"""
        return (datetime.now() - self.fetched_at).total_seconds()

    @property
    def is_fresh(self) -> bool:
        """Check if data is still within TTL"""
        return self.age_seconds < self.ttl_seconds

    @property
    def freshness_score(self) -> float:
        """
        Calculate freshness score 0-1
        1.0 = just fetched, 0.0 = at or past TTL
        """
        if self.age_seconds >= self.ttl_seconds:
            return 0.0
        return 1.0 - (self.age_seconds / self.ttl_seconds)

    def to_dict(self) -> Dict:
        return {
            'fetched_at': self.fetched_at.isoformat(),
            'source': self.source,
            'source_url': self.source_url,
            'source_timestamp': self.source_timestamp.isoformat() if self.source_timestamp else None,
            'ttl_seconds': self.ttl_seconds,
            'age_seconds': self.age_seconds,
            'is_fresh': self.is_fresh,
            'freshness_score': round(self.freshness_score, 3)
        }


@dataclass
class SourceData:
    """
    Data retrieved from a single source

    Attributes:
        source_name: Name of the source (e.g., 'yahoo_finance')
        source_category: Category of source (market, government, etc.)
        data: The actual data retrieved
        timestamp: DataTimestamp tracking freshness
        confidence: Base confidence in this source (0-1)
        raw_response: Original response for debugging
    """
    source_name: str
    source_category: DataSource
    data: Any
    timestamp: DataTimestamp
    confidence: float = 0.7
    raw_response: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'source_name': self.source_name,
            'source_category': self.source_category.value,
            'data': self.data,
            'timestamp': self.timestamp.to_dict(),
            'confidence': self.confidence
        }


@dataclass
class VerificationResult:
    """
    Result of verification across multiple sources

    Attributes:
        query: Original verification query
        data_type: Type of data being verified
        status: Verification status
        consensus_value: The agreed-upon value (if any)
        confidence_score: Overall confidence 0-10
        sources: List of source data
        discrepancies: List of found discrepancies
        warnings: List of warning messages
        verified_at: Timestamp of verification
    """
    query: str
    data_type: str
    status: VerificationStatus
    consensus_value: Optional[Any] = None
    confidence_score: float = 0.0
    sources: List[SourceData] = field(default_factory=list)
    discrepancies: List[Dict] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verified_at: datetime = field(default_factory=datetime.now)

    @property
    def source_count(self) -> int:
        return len(self.sources)

    @property
    def is_high_confidence(self) -> bool:
        return self.confidence_score >= 7.0

    def to_dict(self) -> Dict:
        return {
            'query': self.query,
            'data_type': self.data_type,
            'status': self.status.value,
            'consensus_value': self.consensus_value,
            'confidence_score': round(self.confidence_score, 2),
            'source_count': self.source_count,
            'sources': [s.to_dict() for s in self.sources],
            'discrepancies': self.discrepancies,
            'warnings': self.warnings,
            'verified_at': self.verified_at.isoformat(),
            'is_high_confidence': self.is_high_confidence
        }


@dataclass
class CrossReferenceResult:
    """
    Result of cross-referencing web and local data

    Attributes:
        matches: Fields that match between sources
        discrepancies: Fields with different values
        web_only: Fields only in web data
        local_only: Fields only in local data
        agreement_score: How much sources agree (0-1)
    """
    matches: Dict[str, Any] = field(default_factory=dict)
    discrepancies: List[Dict] = field(default_factory=list)
    web_only: Dict[str, Any] = field(default_factory=dict)
    local_only: Dict[str, Any] = field(default_factory=dict)
    agreement_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            'matches': self.matches,
            'discrepancies': self.discrepancies,
            'web_only': self.web_only,
            'local_only': self.local_only,
            'agreement_score': round(self.agreement_score, 3)
        }


class VerificationEngine:
    """
    Web-First Empirical Verification Engine

    Verifies data by fetching from multiple trusted sources,
    cross-referencing results, and calculating confidence scores.

    Key principles:
    - Web data takes precedence (web-first)
    - Multiple source agreement = higher confidence
    - Government sources have higher weight
    - Recent data has higher confidence
    - Discrepancies trigger warnings

    Example:
        engine = VerificationEngine()

        # Verify a stock price
        result = await engine.verify_price("AAPL")
        print(f"Price: ${result.consensus_value}, Confidence: {result.confidence_score}/10")

        # Cross-reference web vs local data
        discrepancies = engine.cross_reference(web_data, local_data)
    """

    # Trusted source definitions with weights
    TRUSTED_SOURCES = {
        DataSource.MARKET: {
            'yahoo_finance': {'url': 'finance.yahoo.com', 'weight': 0.9},
            'bloomberg': {'url': 'bloomberg.com', 'weight': 0.95},
            'reuters': {'url': 'reuters.com', 'weight': 0.9},
        },
        DataSource.GOVERNMENT: {
            'federal_reserve': {'url': 'federalreserve.gov', 'weight': 1.0},
            'fred': {'url': 'fred.stlouisfed.org', 'weight': 1.0},
            'bls': {'url': 'bls.gov', 'weight': 1.0},
            'sec': {'url': 'sec.gov', 'weight': 1.0},
        },
        DataSource.OPTIONS: {
            'menthorq': {'url': 'menthorq.com', 'weight': 0.85},
            'cboe': {'url': 'cboe.com', 'weight': 0.95},
            'barchart': {'url': 'barchart.com', 'weight': 0.85},
        },
        DataSource.NEWS: {
            'reuters_news': {'url': 'reuters.com', 'weight': 0.9},
            'bloomberg_news': {'url': 'bloomberg.com', 'weight': 0.9},
            'wsj': {'url': 'wsj.com', 'weight': 0.9},
        },
    }

    # TTL by data type (seconds)
    DATA_TTL = {
        'price': 60,           # 1 minute
        'quote': 60,           # 1 minute
        'options': 300,        # 5 minutes
        'filing': 3600,        # 1 hour
        'event': 3600,         # 1 hour
        'economic': 86400,     # 1 day
        'news': 300,           # 5 minutes
        'default': 300,        # 5 minutes default
    }

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """
        Initialize the Verification Engine

        Args:
            session: Optional aiohttp session for connection reuse
        """
        self._session = session
        self._owns_session = session is None
        self._cache: Dict[str, Tuple[VerificationResult, datetime]] = {}
        self._cache_ttl = 60  # Cache results for 60 seconds

        # Local knowledge paths
        self.base_path = config.base_path
        self.lead_quant_patterns = [
            "LEAD_QUANT_*.md",
            "LEAD_QUANT_*.py",
        ]
        self.lead_inventor_patterns = [
            "LEAD_INVENTOR_*.md",
            "LEAD_INVENTOR_*.py",
        ]

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session

    async def close(self):
        """Close the session if we own it"""
        if self._owns_session and self._session:
            await self._session.close()
            self._session = None

    def _get_cache_key(self, query: str, data_type: str) -> str:
        """Generate cache key for query"""
        raw = f"{query}:{data_type}".lower()
        return hashlib.md5(raw.encode()).hexdigest()

    def _check_cache(self, query: str, data_type: str) -> Optional[VerificationResult]:
        """Check if result is cached and fresh"""
        key = self._get_cache_key(query, data_type)
        if key in self._cache:
            result, cached_at = self._cache[key]
            if (datetime.now() - cached_at).total_seconds() < self._cache_ttl:
                return result
            else:
                del self._cache[key]
        return None

    def _set_cache(self, query: str, data_type: str, result: VerificationResult):
        """Cache a verification result"""
        key = self._get_cache_key(query, data_type)
        self._cache[key] = (result, datetime.now())

    # ========================================================================
    # MAIN VERIFICATION METHODS
    # ========================================================================

    async def verify_web_first(
        self,
        query: str,
        data_type: str,
        sources: Optional[List[DataSource]] = None
    ) -> VerificationResult:
        """
        Verify data using web sources first, with local fallback

        This is the primary verification method. It fetches data from multiple
        trusted web sources, cross-references them, and calculates confidence.

        Args:
            query: The verification query (e.g., ticker symbol, event name)
            data_type: Type of data (price, event, filing, etc.)
            sources: Optional list of source categories to use

        Returns:
            VerificationResult with consensus value and confidence score

        Example:
            result = await engine.verify_web_first("AAPL", "price")
            if result.is_high_confidence:
                print(f"Verified price: ${result.consensus_value}")
        """
        # Check cache first
        cached = self._check_cache(query, data_type)
        if cached:
            return cached

        # Determine which sources to query
        if sources is None:
            sources = self._select_sources_for_type(data_type)

        # Fetch from all sources in parallel
        source_data = await self._fetch_from_sources(query, data_type, sources)

        # Calculate consensus and confidence
        result = self._calculate_verification_result(query, data_type, source_data)

        # Cache the result
        self._set_cache(query, data_type, result)

        return result

    def cross_reference(
        self,
        web_data: Dict[str, Any],
        local_data: Dict[str, Any],
        tolerance: float = 0.01
    ) -> CrossReferenceResult:
        """
        Cross-reference web data against local data to find discrepancies

        Compares each field in both data sets and identifies:
        - Matches: Fields that agree (within tolerance for numbers)
        - Discrepancies: Fields with different values
        - Web-only: Fields only in web data
        - Local-only: Fields only in local data

        Args:
            web_data: Data from web sources
            local_data: Data from local sources
            tolerance: Tolerance for numeric comparison (default 1%)

        Returns:
            CrossReferenceResult with detailed comparison

        Example:
            result = engine.cross_reference(
                {'price': 150.25, 'volume': 1000000},
                {'price': 150.00, 'volume': 1000000}
            )
            # result.discrepancies = [{'field': 'price', 'web': 150.25, 'local': 150.00}]
        """
        result = CrossReferenceResult()

        all_keys: Set[str] = set(web_data.keys()) | set(local_data.keys())
        match_count = 0
        total_comparable = 0

        for key in all_keys:
            in_web = key in web_data
            in_local = key in local_data

            if in_web and in_local:
                total_comparable += 1
                web_val = web_data[key]
                local_val = local_data[key]

                if self._values_match(web_val, local_val, tolerance):
                    result.matches[key] = web_val
                    match_count += 1
                else:
                    result.discrepancies.append({
                        'field': key,
                        'web_value': web_val,
                        'local_value': local_val,
                        'difference': self._calculate_difference(web_val, local_val)
                    })
            elif in_web:
                result.web_only[key] = web_data[key]
            else:
                result.local_only[key] = local_data[key]

        # Calculate agreement score
        if total_comparable > 0:
            result.agreement_score = match_count / total_comparable
        else:
            result.agreement_score = 0.0

        return result

    def get_confidence_score(
        self,
        sources: List[SourceData],
        require_government: bool = False
    ) -> Tuple[float, List[str]]:
        """
        Calculate overall confidence score from multiple sources

        Confidence factors:
        - Number of sources (more = higher)
        - Source category weights (government = highest)
        - Data freshness
        - Source agreement

        Args:
            sources: List of SourceData from different sources
            require_government: Whether to require government source for high confidence

        Returns:
            Tuple of (confidence_score 0-10, list of scoring factors)

        Example:
            score, factors = engine.get_confidence_score(sources)
            print(f"Confidence: {score}/10")
            for factor in factors:
                print(f"  {factor}")
        """
        if not sources:
            return 0.0, ["[!] No sources available"]

        factors = []
        score = 0.0

        # Factor 1: Number of sources (max 2 points)
        source_count_score = min(2.0, len(sources) * 0.5)
        score += source_count_score
        factors.append(f"[>] Source count: {len(sources)} sources (+{source_count_score:.1f})")

        # Factor 2: Source category weights (max 3 points)
        category_score = 0.0
        has_government = False
        for source in sources:
            source_config = self._get_source_config(source.source_name, source.source_category)
            weight = source_config.get('weight', 0.7) if source_config else 0.7
            category_score += weight
            if source.source_category == DataSource.GOVERNMENT:
                has_government = True

        avg_weight = category_score / len(sources)
        weighted_score = avg_weight * 3.0
        score += weighted_score
        factors.append(f"[>] Source quality: avg weight {avg_weight:.2f} (+{weighted_score:.1f})")

        if has_government:
            factors.append("[+] Government source present")
        elif require_government:
            score -= 1.0
            factors.append("[-] No government source (-1.0)")

        # Factor 3: Data freshness (max 2 points)
        freshness_scores = [s.timestamp.freshness_score for s in sources]
        avg_freshness = sum(freshness_scores) / len(freshness_scores)
        freshness_score = avg_freshness * 2.0
        score += freshness_score
        factors.append(f"[>] Data freshness: {avg_freshness:.0%} (+{freshness_score:.1f})")

        # Factor 4: Source agreement (max 3 points)
        if len(sources) >= 2:
            agreement = self._calculate_source_agreement(sources)
            agreement_score = agreement * 3.0
            score += agreement_score
            factors.append(f"[>] Source agreement: {agreement:.0%} (+{agreement_score:.1f})")
        else:
            factors.append("[!] Single source - cannot verify agreement")

        # Clamp to 0-10
        final_score = max(0.0, min(10.0, score))

        return round(final_score, 2), factors

    # ========================================================================
    # SPECIFIC VERIFICATION METHODS
    # ========================================================================

    async def verify_price(self, ticker: str) -> VerificationResult:
        """
        Verify current price for a ticker from multiple sources

        Fetches price data from Yahoo Finance, Bloomberg, Reuters and
        cross-references to ensure accuracy.

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")

        Returns:
            VerificationResult with verified price and confidence

        Example:
            result = await engine.verify_price("AAPL")
            if result.status == VerificationStatus.VERIFIED:
                print(f"AAPL price: ${result.consensus_value}")
        """
        return await self.verify_web_first(
            query=ticker.upper(),
            data_type="price",
            sources=[DataSource.MARKET]
        )

    async def verify_event(
        self,
        event_name: str,
        event_date: Optional[datetime] = None
    ) -> VerificationResult:
        """
        Verify event details (earnings, Fed meetings, etc.)

        Args:
            event_name: Name of the event (e.g., "FOMC meeting", "AAPL earnings")
            event_date: Optional expected date to verify

        Returns:
            VerificationResult with event details and confidence

        Example:
            result = await engine.verify_event("FOMC meeting")
            print(f"Next FOMC: {result.consensus_value['date']}")
        """
        sources = [DataSource.NEWS]
        if "fed" in event_name.lower() or "fomc" in event_name.lower():
            sources.append(DataSource.GOVERNMENT)

        result = await self.verify_web_first(
            query=event_name,
            data_type="event",
            sources=sources
        )

        # Add date verification if provided
        if event_date and result.consensus_value:
            expected_str = event_date.strftime("%Y-%m-%d")
            if 'date' in result.consensus_value:
                actual_str = result.consensus_value.get('date', '')
                if expected_str != actual_str:
                    result.warnings.append(
                        f"[!] Date mismatch: expected {expected_str}, got {actual_str}"
                    )

        return result

    async def verify_filing(self, ticker: str) -> VerificationResult:
        """
        Check latest SEC filings for a ticker

        Fetches recent 10-K, 10-Q, 8-K filings from SEC EDGAR
        and verifies filing dates and types.

        Args:
            ticker: Stock ticker symbol

        Returns:
            VerificationResult with filing information

        Example:
            result = await engine.verify_filing("AAPL")
            for filing in result.consensus_value['recent_filings']:
                print(f"{filing['type']}: {filing['date']}")
        """
        return await self.verify_web_first(
            query=ticker.upper(),
            data_type="filing",
            sources=[DataSource.GOVERNMENT]  # SEC is government
        )

    def search_local_knowledge(
        self,
        query: str,
        include_lead_quant: bool = True,
        include_lead_inventor: bool = True
    ) -> List[Dict]:
        """
        Search Lead Quant and Lead Inventor files for local knowledge

        Searches markdown and Python files for relevant information
        based on the query. Useful for finding thesis context and
        historical analysis.

        Args:
            query: Search query (ticker, thesis term, etc.)
            include_lead_quant: Search Lead Quant files
            include_lead_inventor: Search Lead Inventor files

        Returns:
            List of matching results with file path, snippet, and relevance

        Example:
            results = engine.search_local_knowledge("uranium thesis")
            for r in results:
                print(f"{r['file']}: {r['snippet'][:100]}...")
        """
        results = []
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        patterns = []
        if include_lead_quant:
            patterns.extend(self.lead_quant_patterns)
        if include_lead_inventor:
            patterns.extend(self.lead_inventor_patterns)

        # Search files matching patterns
        for pattern in patterns:
            for file_path in self.base_path.glob(pattern):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    content_lower = content.lower()

                    # Check for query term matches
                    matches = sum(1 for term in query_terms if term in content_lower)
                    if matches > 0:
                        # Extract relevant snippet
                        snippet = self._extract_snippet(content, query_terms)
                        relevance = matches / len(query_terms) if query_terms else 0

                        results.append({
                            'file': str(file_path.name),
                            'path': str(file_path),
                            'snippet': snippet,
                            'relevance': relevance,
                            'matches': matches,
                            'source': 'lead_quant' if 'QUANT' in pattern else 'lead_inventor'
                        })
                except Exception:
                    continue

        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)

        return results[:10]  # Return top 10

    # ========================================================================
    # ASYNC PARALLEL VERIFICATION
    # ========================================================================

    async def verify_multiple(
        self,
        queries: List[Tuple[str, str]]
    ) -> Dict[str, VerificationResult]:
        """
        Verify multiple queries in parallel

        Executes multiple verifications concurrently for better performance.

        Args:
            queries: List of (query, data_type) tuples

        Returns:
            Dict mapping query to VerificationResult

        Example:
            results = await engine.verify_multiple([
                ("AAPL", "price"),
                ("MSFT", "price"),
                ("FOMC meeting", "event")
            ])
        """
        tasks = [
            self.verify_web_first(query, data_type)
            for query, data_type in queries
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            queries[i][0]: result if not isinstance(result, Exception)
            else self._create_error_result(queries[i][0], queries[i][1], str(result))
            for i, result in enumerate(results)
        }

    async def verify_with_timeout(
        self,
        query: str,
        data_type: str,
        timeout_seconds: float = 30.0
    ) -> VerificationResult:
        """
        Verify with timeout to prevent hanging

        Args:
            query: Verification query
            data_type: Type of data
            timeout_seconds: Maximum time to wait

        Returns:
            VerificationResult or timeout error result
        """
        try:
            result = await asyncio.wait_for(
                self.verify_web_first(query, data_type),
                timeout=timeout_seconds
            )
            return result
        except asyncio.TimeoutError:
            return self._create_error_result(
                query, data_type,
                f"Verification timed out after {timeout_seconds}s"
            )

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _select_sources_for_type(self, data_type: str) -> List[DataSource]:
        """Select appropriate sources for data type"""
        source_map = {
            'price': [DataSource.MARKET],
            'quote': [DataSource.MARKET],
            'options': [DataSource.OPTIONS, DataSource.MARKET],
            'filing': [DataSource.GOVERNMENT],
            'event': [DataSource.NEWS, DataSource.GOVERNMENT],
            'economic': [DataSource.GOVERNMENT],
            'news': [DataSource.NEWS],
        }
        return source_map.get(data_type, [DataSource.MARKET, DataSource.NEWS])

    def _get_source_config(
        self,
        source_name: str,
        category: DataSource
    ) -> Optional[Dict]:
        """Get configuration for a specific source"""
        category_sources = self.TRUSTED_SOURCES.get(category, {})
        return category_sources.get(source_name)

    async def _fetch_from_sources(
        self,
        query: str,
        data_type: str,
        sources: List[DataSource]
    ) -> List[SourceData]:
        """Fetch data from multiple sources in parallel"""
        tasks = []

        for source_category in sources:
            category_sources = self.TRUSTED_SOURCES.get(source_category, {})
            for source_name, source_config in category_sources.items():
                tasks.append(
                    self._fetch_single_source(
                        query, data_type, source_name, source_category, source_config
                    )
                )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and None results
        valid_results = [
            r for r in results
            if r is not None and not isinstance(r, Exception)
        ]

        return valid_results

    async def _fetch_single_source(
        self,
        query: str,
        data_type: str,
        source_name: str,
        source_category: DataSource,
        source_config: Dict
    ) -> Optional[SourceData]:
        """
        Fetch data from a single source

        Note: In production, this would make actual HTTP requests.
        This implementation simulates responses for demonstration.
        """
        try:
            # Simulate fetch delay
            await asyncio.sleep(0.1)

            # Generate simulated data based on source and type
            # In production, this would be actual HTTP requests
            data = self._simulate_source_response(
                query, data_type, source_name, source_category
            )

            if data is None:
                return None

            ttl = self.DATA_TTL.get(data_type, self.DATA_TTL['default'])

            return SourceData(
                source_name=source_name,
                source_category=source_category,
                data=data,
                timestamp=DataTimestamp(
                    fetched_at=datetime.now(),
                    source=source_name,
                    source_url=source_config.get('url', ''),
                    ttl_seconds=ttl
                ),
                confidence=source_config.get('weight', 0.7)
            )
        except Exception:
            return None

    def _simulate_source_response(
        self,
        query: str,
        data_type: str,
        source_name: str,
        source_category: DataSource
    ) -> Optional[Dict]:
        """
        Simulate source response for demonstration

        In production, replace with actual API calls to:
        - Yahoo Finance API
        - SEC EDGAR API
        - FRED API
        - News APIs
        """
        # This is a placeholder that would be replaced with actual API calls
        if data_type == "price":
            # Simulate price data with slight variation
            base_price = hash(query) % 1000 + 50
            variation = (hash(source_name) % 100) / 1000
            return {
                'ticker': query.upper(),
                'price': round(base_price * (1 + variation), 2),
                'change': round((hash(query + source_name) % 100 - 50) / 10, 2),
                'volume': hash(query) % 10000000
            }
        elif data_type == "event":
            return {
                'event': query,
                'date': '2026-01-29',  # Simulated next event date
                'type': 'scheduled',
                'confirmed': source_category == DataSource.GOVERNMENT
            }
        elif data_type == "filing":
            return {
                'ticker': query.upper(),
                'recent_filings': [
                    {'type': '10-Q', 'date': '2025-11-15'},
                    {'type': '8-K', 'date': '2025-10-28'},
                ],
                'last_updated': datetime.now().isoformat()
            }

        return {'query': query, 'source': source_name}

    def _calculate_verification_result(
        self,
        query: str,
        data_type: str,
        sources: List[SourceData]
    ) -> VerificationResult:
        """Calculate final verification result from sources"""
        if not sources:
            return VerificationResult(
                query=query,
                data_type=data_type,
                status=VerificationStatus.FAILED,
                warnings=["[!] No sources returned data"]
            )

        # Calculate confidence
        confidence, factors = self.get_confidence_score(sources)

        # Determine consensus value
        consensus_value = self._determine_consensus(sources, data_type)

        # Check for discrepancies
        discrepancies = self._find_discrepancies(sources, data_type)

        # Determine status
        if len(sources) >= 2 and not discrepancies:
            status = VerificationStatus.VERIFIED
        elif len(sources) >= 2 and discrepancies:
            status = VerificationStatus.PARTIALLY_VERIFIED
        elif len(sources) == 1:
            status = VerificationStatus.UNVERIFIED
        else:
            status = VerificationStatus.FAILED

        # Check freshness
        stale_sources = [s for s in sources if not s.timestamp.is_fresh]
        warnings = []
        if stale_sources:
            status = VerificationStatus.STALE
            warnings.append(f"[!] {len(stale_sources)} source(s) have stale data")

        # Add confidence factors as insights
        warnings.extend(factors)

        return VerificationResult(
            query=query,
            data_type=data_type,
            status=status,
            consensus_value=consensus_value,
            confidence_score=confidence,
            sources=sources,
            discrepancies=discrepancies,
            warnings=warnings
        )

    def _determine_consensus(
        self,
        sources: List[SourceData],
        data_type: str
    ) -> Optional[Any]:
        """Determine consensus value from multiple sources"""
        if not sources:
            return None

        if len(sources) == 1:
            return sources[0].data

        # For price data, use weighted average
        if data_type == "price":
            prices = []
            weights = []
            for s in sources:
                if isinstance(s.data, dict) and 'price' in s.data:
                    prices.append(s.data['price'])
                    weights.append(s.confidence)

            if prices:
                weighted_avg = sum(p * w for p, w in zip(prices, weights)) / sum(weights)
                base_data = sources[0].data.copy()
                base_data['price'] = round(weighted_avg, 2)
                base_data['source_count'] = len(sources)
                return base_data

        # For other types, use the highest confidence source
        best_source = max(sources, key=lambda s: s.confidence)
        return best_source.data

    def _find_discrepancies(
        self,
        sources: List[SourceData],
        data_type: str
    ) -> List[Dict]:
        """Find discrepancies between sources"""
        if len(sources) < 2:
            return []

        discrepancies = []

        if data_type == "price":
            prices = []
            for s in sources:
                if isinstance(s.data, dict) and 'price' in s.data:
                    prices.append((s.source_name, s.data['price']))

            if len(prices) >= 2:
                # Check for significant price differences (> 1%)
                for i, (name1, price1) in enumerate(prices):
                    for name2, price2 in prices[i+1:]:
                        diff_pct = abs(price1 - price2) / max(price1, price2)
                        if diff_pct > 0.01:
                            discrepancies.append({
                                'field': 'price',
                                'source1': name1,
                                'value1': price1,
                                'source2': name2,
                                'value2': price2,
                                'difference_pct': round(diff_pct * 100, 2)
                            })

        return discrepancies

    def _calculate_source_agreement(self, sources: List[SourceData]) -> float:
        """Calculate how much sources agree (0-1)"""
        if len(sources) < 2:
            return 1.0

        # Compare data from each pair of sources
        agreements = 0
        comparisons = 0

        for i, s1 in enumerate(sources):
            for s2 in sources[i+1:]:
                comparisons += 1
                if self._data_agrees(s1.data, s2.data):
                    agreements += 1

        return agreements / comparisons if comparisons > 0 else 0.0

    def _data_agrees(self, data1: Any, data2: Any, tolerance: float = 0.01) -> bool:
        """Check if two data values agree"""
        if isinstance(data1, dict) and isinstance(data2, dict):
            # For price data, check price field
            if 'price' in data1 and 'price' in data2:
                diff = abs(data1['price'] - data2['price'])
                avg = (data1['price'] + data2['price']) / 2
                return (diff / avg) <= tolerance
            return True  # Other dict fields assumed to agree

        return data1 == data2

    def _values_match(
        self,
        val1: Any,
        val2: Any,
        tolerance: float = 0.01
    ) -> bool:
        """Check if two values match within tolerance"""
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if val1 == 0 and val2 == 0:
                return True
            avg = (abs(val1) + abs(val2)) / 2
            if avg == 0:
                return val1 == val2
            return abs(val1 - val2) / avg <= tolerance

        return val1 == val2

    def _calculate_difference(self, val1: Any, val2: Any) -> Optional[str]:
        """Calculate difference between two values"""
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            diff = val1 - val2
            if val2 != 0:
                pct = (diff / val2) * 100
                return f"{diff:+.2f} ({pct:+.2f}%)"
            return f"{diff:+.2f}"

        return None

    def _extract_snippet(self, content: str, query_terms: Set[str], max_length: int = 200) -> str:
        """Extract relevant snippet from content"""
        content_lower = content.lower()

        # Find first occurrence of any query term
        first_pos = len(content)
        for term in query_terms:
            pos = content_lower.find(term)
            if pos != -1 and pos < first_pos:
                first_pos = pos

        if first_pos == len(content):
            first_pos = 0

        # Extract snippet around the match
        start = max(0, first_pos - 50)
        end = min(len(content), first_pos + max_length)

        snippet = content[start:end].strip()

        # Clean up
        snippet = re.sub(r'\s+', ' ', snippet)

        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet

    def _create_error_result(
        self,
        query: str,
        data_type: str,
        error: str
    ) -> VerificationResult:
        """Create an error verification result"""
        return VerificationResult(
            query=query,
            data_type=data_type,
            status=VerificationStatus.FAILED,
            warnings=[f"[!] Error: {error}"]
        )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def print_verification_report(self, result: VerificationResult) -> str:
        """
        Generate a printable verification report

        Args:
            result: VerificationResult to format

        Returns:
            Formatted string report
        """
        lines = [
            "=" * 70,
            f"VERIFICATION REPORT - {result.query}",
            "=" * 70,
            "",
            f"[*] STATUS: {result.status.value.upper()}",
            f"[*] CONFIDENCE: {result.confidence_score}/10",
            f"[*] DATA TYPE: {result.data_type}",
            f"[*] SOURCES: {result.source_count}",
            "",
        ]

        if result.consensus_value:
            lines.append("CONSENSUS VALUE:")
            lines.append(f"  {json.dumps(result.consensus_value, indent=2, default=str)}")
            lines.append("")

        if result.discrepancies:
            lines.append("DISCREPANCIES:")
            for d in result.discrepancies:
                lines.append(f"  - {d}")
            lines.append("")

        if result.warnings:
            lines.append("FACTORS & WARNINGS:")
            for w in result.warnings:
                lines.append(f"  {w}")
            lines.append("")

        lines.extend(["=" * 70])

        return "\n".join(lines)

    def clear_cache(self):
        """Clear the verification cache"""
        self._cache.clear()


# Convenience function for quick verification
async def quick_verify(
    query: str,
    data_type: str = "price"
) -> VerificationResult:
    """
    Quick verification without managing engine lifecycle

    Args:
        query: What to verify (ticker, event, etc.)
        data_type: Type of data (price, event, filing)

    Returns:
        VerificationResult

    Example:
        result = await quick_verify("AAPL", "price")
        print(f"Verified: {result.consensus_value}")
    """
    engine = VerificationEngine()
    try:
        return await engine.verify_web_first(query, data_type)
    finally:
        await engine.close()
