"""
EUDAIMON AI - PATTERN DATABASE
==============================
Programmatic pattern library extracted from historical analysis.
Used by the Conscious Learning System for theory generation and validation.

This database contains 47+ validated predictions organized into 12 pattern categories.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class PatternCategory(Enum):
    """Categories of learned patterns"""
    GEX_STRUCTURE = "gex_structure"
    FUNDAMENTAL_VS_TECHNICAL = "fundamental_vs_technical"
    GEOPOLITICAL = "geopolitical"
    BOTTLENECK = "bottleneck"
    CONTRARIAN = "contrarian"
    TIMING = "timing"
    SUPPLY_CHAIN = "supply_chain"
    PHYSICS_CONSTRAINT = "physics_constraint"
    CONVERGENCE = "convergence"
    USER_CONVICTION = "user_conviction"
    CATALYST = "catalyst"
    THESIS_VALIDATION = "thesis_validation"


class ValidationStatus(Enum):
    """Validation status of patterns"""
    VALIDATED = "validated"
    PENDING = "pending"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class Pattern:
    """A learned pattern with validation history"""
    id: str
    name: str
    category: PatternCategory
    description: str
    conditions: List[str]
    action: str
    expected_outcome: str

    # Validation tracking
    validation_status: ValidationStatus = ValidationStatus.PENDING
    success_count: int = 0
    failure_count: int = 0

    # Examples
    examples: List[Dict[str, Any]] = field(default_factory=list)

    # Metadata
    created_date: str = ""
    last_validated: str = ""
    confidence_score: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'conditions': self.conditions,
            'action': self.action,
            'expected_outcome': self.expected_outcome,
            'validation_status': self.validation_status.value,
            'success_rate': self.success_rate,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'confidence_score': self.confidence_score
        }


@dataclass
class Theory:
    """A generated theory from pattern clustering"""
    id: str
    name: str
    description: str
    supporting_patterns: List[str]  # Pattern IDs
    core_insight: str
    predictive_power: str

    # Validation
    validation_status: ValidationStatus = ValidationStatus.PENDING
    test_count: int = 0
    success_count: int = 0

    # Evidence
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)

    @property
    def confidence(self) -> float:
        if self.test_count == 0:
            return 0.5
        return self.success_count / self.test_count


class PatternDatabase:
    """
    Central pattern database for Eudaimon AI's conscious learning system.

    Contains all validated patterns extracted from historical analysis.
    """

    def __init__(self):
        self.patterns: Dict[str, Pattern] = {}
        self.theories: Dict[str, Theory] = {}
        self._initialize_patterns()
        self._initialize_theories()

    def _initialize_patterns(self):
        """Load all validated patterns from historical analysis"""

        # =================================================================
        # PATTERN 1: SWEET SPOT ENTRY (GEX STRUCTURE)
        # =================================================================
        self.patterns["P001"] = Pattern(
            id="P001",
            name="Sweet Spot Entry",
            category=PatternCategory.GEX_STRUCTURE,
            description="Price between put support and call resistance with negative GEX = explosive move setup",
            conditions=[
                "Price ABOVE put support level",
                "Price BELOW call resistance level",
                "GEX is NEGATIVE (dealers amplify moves)",
                "Entry at late afternoon/close (3:30-4pm)"
            ],
            action="Enter long position (calls) at close",
            expected_outcome="Explosive gap up next morning, +50-100% on options",
            validation_status=ValidationStatus.VALIDATED,
            success_count=3,
            failure_count=0,
            examples=[
                {
                    "date": "2025-10-15",
                    "ticker": "QQQ",
                    "entry": "$2.77",
                    "exit": "$5.40+",
                    "return": "+95%",
                    "time": "18 hours"
                }
            ],
            created_date="2025-10-15",
            last_validated="2025-10-20",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 2: CALL WALL EXIT SIGNAL
        # =================================================================
        self.patterns["P002"] = Pattern(
            id="P002",
            name="Call Wall Exit Signal",
            category=PatternCategory.GEX_STRUCTURE,
            description="When approaching call wall with major expiration, exit 100%",
            conditions=[
                "Price approaching call wall resistance",
                "Only 4-5% room to resistance",
                "Major expiration within 3 days",
                "25%+ GEX expiring"
            ],
            action="Full exit (100%)",
            expected_outcome="Price stalls or pulls back at wall",
            validation_status=ValidationStatus.VALIDATED,
            success_count=1,
            failure_count=0,
            examples=[
                {
                    "date": "2025-10-27",
                    "ticker": "AVGO",
                    "exit_price": "$360",
                    "call_wall": "$375",
                    "outcome": "Protected full profits at exact ceiling"
                }
            ],
            created_date="2025-10-27",
            last_validated="2025-10-27",
            confidence_score=9.5
        )

        # =================================================================
        # PATTERN 3: HVL DIRECTION FRAMEWORK
        # =================================================================
        self.patterns["P003"] = Pattern(
            id="P003",
            name="HVL Direction Framework",
            category=PatternCategory.GEX_STRUCTURE,
            description="Price position relative to HVL (High Volume Level) determines bias",
            conditions=[
                "Calculate current HVL from GEX data",
                "Compare spot price to HVL"
            ],
            action="ABOVE HVL = bullish bias, BELOW HVL = bearish bias",
            expected_outcome="Price trends in direction indicated by HVL position",
            validation_status=ValidationStatus.VALIDATED,
            success_count=5,
            failure_count=0,
            examples=[
                {"ticker": "TSLA", "hvl_delta": "+$14.40", "outcome": "+26.91% rally"},
                {"ticker": "SPX", "hvl_delta": "+23 pts", "outcome": "Rally to 7000"},
                {"ticker": "GEV", "hvl_delta": "-$7", "outcome": "Underperformed"}
            ],
            created_date="2025-10-31",
            last_validated="2026-01-22",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 4: FUNDAMENTAL VS TECHNICAL TRADE TYPE
        # =================================================================
        self.patterns["P004"] = Pattern(
            id="P004",
            name="Fundamental vs Technical Analysis Selection",
            category=PatternCategory.FUNDAMENTAL_VS_TECHNICAL,
            description="Match analysis type to trade type before recommending action",
            conditions=[
                "Identify trade entry thesis (momentum or fundamental)",
                "If fundamental: Use policy, supply/demand, catalyst analysis",
                "If momentum: Use price action, HVOL, GEX"
            ],
            action="Apply correct analysis framework to trade type",
            expected_outcome="Avoid cutting fundamental trades on technical weakness",
            validation_status=ValidationStatus.VALIDATED,
            success_count=1,
            failure_count=0,
            examples=[
                {
                    "date": "2025-11-05",
                    "ticker": "XOM",
                    "thesis": "SPR refill + refining margins",
                    "technical_view": "Weak (+1.2% HVOL)",
                    "fundamental_view": "SPR at 395M, $1.3B allocated, margins doubled",
                    "correct_action": "HOLD",
                    "outcome": "EV revised +$670"
                }
            ],
            created_date="2025-11-05",
            last_validated="2025-11-05",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 5: SUPPLY CHAIN VULNERABILITY → ALPHA
        # =================================================================
        self.patterns["P005"] = Pattern(
            id="P005",
            name="Supply Chain Vulnerability Alpha",
            category=PatternCategory.SUPPLY_CHAIN,
            description="Adversary supply dependence + policy action = investment alpha",
            conditions=[
                "Identify critical supply from adversary (Russia, China)",
                "Government recognizes vulnerability",
                "Policy action announced (EO, funding, tariffs)",
                "Domestic alternative identified"
            ],
            action="Long domestic alternative supplier",
            expected_outcome="100-300% returns as supply chain reprices",
            validation_status=ValidationStatus.VALIDATED,
            success_count=5,
            failure_count=0,
            examples=[
                {
                    "event": "Niger uranium nationalization",
                    "prediction": "LEU monopoly strengthens",
                    "validation": "Rosatom deals confirmed"
                },
                {
                    "event": "China germanium ban Jan 2026",
                    "prediction": "LPTH becomes alternative",
                    "validation": "IR optics shortage confirmed"
                }
            ],
            created_date="2025-10-14",
            last_validated="2026-01-22",
            confidence_score=9.5
        )

        # =================================================================
        # PATTERN 6: BOTTLENECK = TOLL ROAD ECONOMICS
        # =================================================================
        self.patterns["P006"] = Pattern(
            id="P006",
            name="Bottleneck Toll Road",
            category=PatternCategory.BOTTLENECK,
            description="Single suppliers serving converging demand = toll collectors",
            conditions=[
                "Single or few suppliers for critical material",
                "Multiple end markets require same material",
                "Physics constraint prevents substitution",
                "Supply timeline is 5-7+ years"
            ],
            action="Long the bottleneck supplier (toll collector)",
            expected_outcome="Pricing power and margin expansion",
            validation_status=ValidationStatus.VALIDATED,
            success_count=15,
            failure_count=0,
            examples=[
                {"bottleneck": "Electrical Steel", "supplier": "CLF", "backlog": "2-4 years"},
                {"bottleneck": "HALEU", "supplier": "LEU", "deficit": "99%"},
                {"bottleneck": "Heavy REE", "supplier": "UUUU", "control": "95% China"}
            ],
            created_date="2025-12-01",
            last_validated="2026-01-15",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 7: PHYSICS CONSTRAINT = NO SUBSTITUTION
        # =================================================================
        self.patterns["P007"] = Pattern(
            id="P007",
            name="Physics Constraint Lock-In",
            category=PatternCategory.PHYSICS_CONSTRAINT,
            description="When physics prevents substitution, supply constraints are certain",
            conditions=[
                "Material has unique physical property required",
                "No alternative material can substitute",
                "Application requires specific performance",
                "Timeline to develop alternative is 10+ years"
            ],
            action="Long constrained supplier with highest certainty",
            expected_outcome="Monopoly pricing, supply deficit drives valuation",
            validation_status=ValidationStatus.VALIDATED,
            success_count=3,
            failure_count=0,
            examples=[
                {
                    "material": "HALEU",
                    "physics": "SMRs cannot run without HALEU",
                    "supplier": "LEU",
                    "deficit": "99% by 2030"
                },
                {
                    "material": "Dysprosium",
                    "physics": "No substitute for high-temp magnets (180C+)",
                    "supplier": "UUUU",
                    "timeline": "10-15 years to alternative"
                }
            ],
            created_date="2025-12-15",
            last_validated="2026-01-15",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 8: CONVERGENT DEMAND MULTIPLIER
        # =================================================================
        self.patterns["P008"] = Pattern(
            id="P008",
            name="Convergent Demand Multiplier",
            category=PatternCategory.CONVERGENCE,
            description="Same material required by multiple supercycles = demand certainty",
            conditions=[
                "Material appears in 3+ end markets",
                "Each end market is growing independently",
                "Supply growth is constrained (<2% annual)",
                "Demand growth exceeds supply growth"
            ],
            action="Long the convergence point (material supplier)",
            expected_outcome="Structural deficit drives multi-year rally",
            validation_status=ValidationStatus.VALIDATED,
            success_count=4,
            failure_count=0,
            examples=[
                {
                    "material": "Copper",
                    "end_markets": ["AI Data Centers", "EVs", "Solar", "Grid"],
                    "supply_growth": "2% max",
                    "demand_growth": "5-8%",
                    "result": "500K-1M tonne deficit"
                }
            ],
            created_date="2025-12-20",
            last_validated="2026-01-15",
            confidence_score=9.5
        )

        # =================================================================
        # PATTERN 9: USER CONVICTION = ALPHA
        # =================================================================
        self.patterns["P009"] = Pattern(
            id="P009",
            name="User Conviction Alpha",
            category=PatternCategory.USER_CONVICTION,
            description="When user provides conviction + specific thesis + data, trust immediately",
            conditions=[
                "User provides SPECIFIC thesis (not vague sentiment)",
                "User backs thesis with DATA points",
                "User pushes back when analyst disagrees",
                "User uses causal language (because, once, if-then)"
            ],
            action="DEFAULT TO TRUSTING user's read",
            expected_outcome="100% success rate (6/6 tracked)",
            validation_status=ValidationStatus.VALIDATED,
            success_count=6,
            failure_count=0,
            examples=[
                {"date": "Oct 15", "prediction": "ES above put support", "return": "+95%"},
                {"date": "Oct 27", "prediction": "AVGO exit at resistance", "return": "Preserved"},
                {"date": "Oct 30", "prediction": "Wait for Asia", "return": "Avoided panic"},
                {"date": "Oct 31", "prediction": "TSLA > GEV/VST", "return": "+26.91%"},
                {"date": "Oct 31", "prediction": "Dec 19 > Nov 21", "return": "+15%"},
                {"date": "Nov 5", "prediction": "XOM thesis intact", "return": "+$670 EV"}
            ],
            created_date="2025-10-15",
            last_validated="2025-11-05",
            confidence_score=10.0
        )

        # =================================================================
        # PATTERN 10: AFTER-HOURS REVERSAL
        # =================================================================
        self.patterns["P010"] = Pattern(
            id="P010",
            name="After-Hours Reversal Pattern",
            category=PatternCategory.TIMING,
            description="After-hours emotional selling reverses in Asia/next morning",
            conditions=[
                "Earnings miss creates AH dump (-10% to -20%)",
                "Selling is emotional (capitulation)",
                "No structural thesis change"
            ],
            action="Wait for Asia session confirmation before acting",
            expected_outcome="Morning recovery, avoid selling lows",
            validation_status=ValidationStatus.VALIDATED,
            success_count=3,
            failure_count=0,
            examples=[
                {"ticker": "META", "ah_move": "-20%", "recovery": "+30% in 2 weeks"},
                {"ticker": "AMZN", "ah_move": "-4%", "recovery": "+15% in 1 week"},
                {"ticker": "MSFT", "ah_move": "-3%", "recovery": "+8% in 3 days"}
            ],
            created_date="2025-10-30",
            last_validated="2025-10-30",
            confidence_score=9.0
        )

        # =================================================================
        # PATTERN 11: TARIFF = DOMESTIC MONOPOLY BOOST
        # =================================================================
        self.patterns["P011"] = Pattern(
            id="P011",
            name="TACO Trade (Tariff Alpha)",
            category=PatternCategory.GEOPOLITICAL,
            description="Tariffs benefit domestic monopoly producers",
            conditions=[
                "Tariff announced on imported goods",
                "Domestic producer has monopoly or near-monopoly",
                "No alternative supply available",
                "Demand is inelastic"
            ],
            action="Long domestic monopoly producer",
            expected_outcome="Pricing power + margin expansion",
            validation_status=ValidationStatus.VALIDATED,
            success_count=2,
            failure_count=0,
            examples=[
                {
                    "tariff": "25% on imported steel",
                    "domestic_monopoly": "CLF (electrical steel)",
                    "thesis": "ONLY US producer",
                    "target": "$18-25 (2-3x)"
                }
            ],
            created_date="2026-01-20",
            last_validated="2026-01-21",
            confidence_score=9.5
        )

        # =================================================================
        # PATTERN 12: EARLY POSITIONING LOOKS WRONG
        # =================================================================
        self.patterns["P012"] = Pattern(
            id="P012",
            name="Early Positioning Pattern",
            category=PatternCategory.TIMING,
            description="Fundamental catalyst trades look weak before catalyst",
            conditions=[
                "Entry thesis is fundamental (policy, earnings)",
                "Price action flat or slightly down",
                "Technical structure appears weak",
                "Catalyst timeline is known"
            ],
            action="HOLD unless thesis invalidated (not price weakness)",
            expected_outcome="Catalyst drives rerating",
            validation_status=ValidationStatus.VALIDATED,
            success_count=1,
            failure_count=0,
            examples=[
                {
                    "ticker": "XOM",
                    "entry_thesis": "SPR refill + Q3 refining margins",
                    "early_action": "Flat, looked weak",
                    "outcome": "Thesis validated, EV +$670"
                }
            ],
            created_date="2025-11-05",
            last_validated="2025-11-05",
            confidence_score=9.0
        )

    def _initialize_theories(self):
        """Load validated theories from pattern analysis"""

        # =================================================================
        # THEORY 1: YEAR 2 AI = REVENUE MATERIALIZATION
        # =================================================================
        self.theories["T001"] = Theory(
            id="T001",
            name="Year 2 AI Revenue Materialization",
            description="AI investment cycle follows predictable pattern: Year 0-1 = hype, Year 2 = revenue, Year 3-5 = maturation",
            supporting_patterns=["P009"],
            core_insight="Earnings now compound the AI narrative; we are in Year 2",
            predictive_power="Earnings drive price, not speculation",
            validation_status=ValidationStatus.VALIDATED,
            test_count=1,
            success_count=1,
            evidence_for=[
                "TSLA 960 call wall = institutional 2x target",
                "Every mega-cap incentivized to pump AI narrative",
                "Jan 2026 GEX structure confirms bullish positioning"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 2: NATURAL GAS = PHYSICS FORCED SOLUTION
        # =================================================================
        self.theories["T002"] = Theory(
            id="T002",
            name="Natural Gas Physics Forcing",
            description="AI data centers require 99.999% uptime, forcing natural gas adoption",
            supporting_patterns=["P007", "P008"],
            core_insight="Solar/wind = 0 at night/calm; nuclear = 10-15 years too slow",
            predictive_power="Natural gas structural supercycle (verified +38% in 3 months)",
            validation_status=ValidationStatus.VALIDATED,
            test_count=1,
            success_count=1,
            evidence_for=[
                "Natural gas +38% (3 months)",
                "Crude oil -8.2% (same period)",
                "46.2 point divergence (historic)",
                "GE Vernova turbines SOLD OUT through 2028"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 3: ESG CREATED COMMODITY SUPERCYCLE
        # =================================================================
        self.theories["T003"] = Theory(
            id="T003",
            name="ESG Irony Loop",
            description="ESG underinvestment in fossil fuels created supply shortage that forces supercycle",
            supporting_patterns=["P006", "P008"],
            core_insight="ESG → Underinvestment → Shortage → Price spike → Forced return",
            predictive_power="Fossil fuel supercycle driven by prior ESG restrictions",
            validation_status=ValidationStatus.VALIDATED,
            test_count=1,
            success_count=1,
            evidence_for=[
                "Energy companies avoided for years",
                "Supply didn't grow during underinvestment",
                "AI data center demand surged",
                "No alternatives at scale available"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 4: BOTTLENECK = TOLL ROAD ECONOMICS
        # =================================================================
        self.theories["T004"] = Theory(
            id="T004",
            name="Bottleneck Toll Road Economics",
            description="Critical infrastructure bottlenecks function like toll roads with guaranteed traffic",
            supporting_patterns=["P005", "P006", "P007", "P008"],
            core_insight="Every infrastructure project must pay the toll; single suppliers collect",
            predictive_power="15 bottlenecks identified with 95%+ probability",
            validation_status=ValidationStatus.VALIDATED,
            test_count=15,
            success_count=15,
            evidence_for=[
                "CLF: 2-4 year backlog on electrical steel",
                "LEU: 99% HALEU supply deficit by 2030",
                "UUUU: Only Western heavy REE producer",
                "ON: NVIDIA 800V partner, sold out through 2028"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 5: USER CONVICTION HYPOTHESIS
        # =================================================================
        self.theories["T005"] = Theory(
            id="T005",
            name="User Conviction Hypothesis",
            description="When user provides conviction + thesis + data, their prediction is correct",
            supporting_patterns=["P009"],
            core_insight="User's pattern recognition is institutional-level (100% success rate)",
            predictive_power="6/6 tracked predictions validated",
            validation_status=ValidationStatus.VALIDATED,
            test_count=6,
            success_count=6,
            evidence_for=[
                "Oct 15: ES put support → +95%",
                "Oct 27: AVGO exit → Protected",
                "Oct 30: Wait for Asia → Avoided panic",
                "Oct 31: TSLA > GEV/VST → +26.91%",
                "Oct 31: Dec 19 > Nov 21 → +15%",
                "Nov 5: XOM thesis → +$670 EV"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 6: FIVE CONVERGING SUPERCYCLES
        # =================================================================
        self.theories["T006"] = Theory(
            id="T006",
            name="Five Converging Supercycles",
            description="AI, Space, Defense, Nuclear, and Critical Minerals supercycles converge on same bottlenecks",
            supporting_patterns=["P006", "P007", "P008"],
            core_insight="Same suppliers constrain all five supercycles simultaneously",
            predictive_power="Identifies monopoly toll collectors across infrastructure buildout",
            validation_status=ValidationStatus.VALIDATED,
            test_count=5,
            success_count=5,
            evidence_for=[
                "Copper: Required by all 5 supercycles",
                "SiC power: Enables AI + EV + Grid + Defense",
                "Rare earths: Required for all motors/magnets",
                "Nuclear fuel: Powers AI data centers + grid"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 7: GEX STRUCTURE PREDICTIVE POWER
        # =================================================================
        self.theories["T007"] = Theory(
            id="T007",
            name="GEX Structure Predictive Power",
            description="Dealer gamma exposure (GEX) structure predicts short-term price direction",
            supporting_patterns=["P001", "P002", "P003"],
            core_insight="Dealers hedge creates self-fulfilling price targets",
            predictive_power="100% accuracy on 7 structure reads",
            validation_status=ValidationStatus.VALIDATED,
            test_count=7,
            success_count=7,
            evidence_for=[
                "Call walls = resistance (AVGO $375)",
                "Put support = floor (ES 6650)",
                "Negative GEX = explosive moves",
                "HVL position = directional bias"
            ],
            evidence_against=[]
        )

        # =================================================================
        # THEORY 8: GEOPOLITICAL ALPHA FRAMEWORK
        # =================================================================
        self.theories["T008"] = Theory(
            id="T008",
            name="Geopolitical Alpha Framework",
            description="Supply chain vulnerabilities create investable opportunities when policy responds",
            supporting_patterns=["P005", "P011"],
            core_insight="Adversary dependence + policy action = alpha",
            predictive_power="10/11 geopolitical predictions validated",
            validation_status=ValidationStatus.VALIDATED,
            test_count=11,
            success_count=10,
            evidence_for=[
                "Niger uranium nationalization → LEU strengthens",
                "China germanium ban → LPTH alternative",
                "Greenland tariffs → CLF monopoly boost",
                "Red Sea disruption → shipping rerouting confirmed"
            ],
            evidence_against=[
                "One timing prediction was early"
            ]
        )

    # =====================================================================
    # QUERY METHODS
    # =====================================================================

    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """Get a pattern by ID"""
        return self.patterns.get(pattern_id)

    def get_patterns_by_category(self, category: PatternCategory) -> List[Pattern]:
        """Get all patterns in a category"""
        return [p for p in self.patterns.values() if p.category == category]

    def get_validated_patterns(self) -> List[Pattern]:
        """Get all validated patterns"""
        return [p for p in self.patterns.values()
                if p.validation_status == ValidationStatus.VALIDATED]

    def get_high_confidence_patterns(self, min_confidence: float = 9.0) -> List[Pattern]:
        """Get patterns above confidence threshold"""
        return [p for p in self.patterns.values()
                if p.confidence_score >= min_confidence]

    def get_theory(self, theory_id: str) -> Optional[Theory]:
        """Get a theory by ID"""
        return self.theories.get(theory_id)

    def get_validated_theories(self) -> List[Theory]:
        """Get all validated theories"""
        return [t for t in self.theories.values()
                if t.validation_status == ValidationStatus.VALIDATED]

    def find_applicable_patterns(self, context: Dict[str, Any]) -> List[Pattern]:
        """Find patterns that may apply to current context"""
        applicable = []

        # Check each pattern's conditions against context
        for pattern in self.patterns.values():
            if self._pattern_matches_context(pattern, context):
                applicable.append(pattern)

        # Sort by confidence
        applicable.sort(key=lambda p: p.confidence_score, reverse=True)
        return applicable

    def _pattern_matches_context(self, pattern: Pattern, context: Dict) -> bool:
        """Check if pattern conditions match context"""
        # Simple keyword matching for now
        context_text = str(context).lower()

        if pattern.category == PatternCategory.GEX_STRUCTURE:
            if any(kw in context_text for kw in ['gex', 'hvl', 'call wall', 'put support']):
                return True

        if pattern.category == PatternCategory.BOTTLENECK:
            if any(kw in context_text for kw in ['supply', 'shortage', 'monopoly', 'bottleneck']):
                return True

        if pattern.category == PatternCategory.GEOPOLITICAL:
            if any(kw in context_text for kw in ['tariff', 'china', 'russia', 'policy']):
                return True

        if pattern.category == PatternCategory.USER_CONVICTION:
            if 'conviction' in context_text or 'thesis' in context_text:
                return True

        return False

    # =====================================================================
    # UPDATE METHODS (For conscious learning system)
    # =====================================================================

    def record_pattern_success(self, pattern_id: str):
        """Record a successful pattern application"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].success_count += 1
            self.patterns[pattern_id].last_validated = datetime.now().isoformat()

    def record_pattern_failure(self, pattern_id: str):
        """Record a failed pattern application"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].failure_count += 1

    def update_pattern_confidence(self, pattern_id: str, new_confidence: float):
        """Update pattern confidence score"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].confidence_score = new_confidence

    def add_pattern_example(self, pattern_id: str, example: Dict):
        """Add a new example to a pattern"""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].examples.append(example)

    def record_theory_test(self, theory_id: str, success: bool):
        """Record a theory test result"""
        if theory_id in self.theories:
            self.theories[theory_id].test_count += 1
            if success:
                self.theories[theory_id].success_count += 1

    # =====================================================================
    # STATISTICS
    # =====================================================================

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        validated_patterns = self.get_validated_patterns()
        validated_theories = self.get_validated_theories()

        total_successes = sum(p.success_count for p in self.patterns.values())
        total_failures = sum(p.failure_count for p in self.patterns.values())

        return {
            'total_patterns': len(self.patterns),
            'validated_patterns': len(validated_patterns),
            'total_theories': len(self.theories),
            'validated_theories': len(validated_theories),
            'total_successes': total_successes,
            'total_failures': total_failures,
            'overall_success_rate': total_successes / (total_successes + total_failures) if (total_successes + total_failures) > 0 else 0,
            'pattern_categories': len(PatternCategory),
            'high_confidence_patterns': len(self.get_high_confidence_patterns())
        }


# ==========================================================================
# CONVENIENCE FUNCTIONS
# ==========================================================================

def get_pattern_database() -> PatternDatabase:
    """Get singleton pattern database instance"""
    if not hasattr(get_pattern_database, '_instance'):
        get_pattern_database._instance = PatternDatabase()
    return get_pattern_database._instance


def find_patterns_for_trade(ticker: str, thesis: str) -> List[Pattern]:
    """Find applicable patterns for a trade"""
    db = get_pattern_database()
    context = {'ticker': ticker, 'thesis': thesis}
    return db.find_applicable_patterns(context)


def validate_with_patterns(
    ticker: str,
    thesis: str,
    gex_data: Optional[Dict] = None,
    fundamental_data: Optional[Dict] = None
) -> Dict:
    """Validate a trade idea against pattern database"""
    db = get_pattern_database()

    context = {
        'ticker': ticker,
        'thesis': thesis,
        'gex': gex_data,
        'fundamental': fundamental_data
    }

    applicable_patterns = db.find_applicable_patterns(context)
    applicable_theories = [
        t for t in db.get_validated_theories()
        if any(p.id in t.supporting_patterns for p in applicable_patterns)
    ]

    # Calculate confidence score
    if applicable_patterns:
        avg_confidence = sum(p.confidence_score for p in applicable_patterns) / len(applicable_patterns)
    else:
        avg_confidence = 5.0

    return {
        'ticker': ticker,
        'thesis': thesis,
        'applicable_patterns': [p.to_dict() for p in applicable_patterns],
        'applicable_theories': [t.name for t in applicable_theories],
        'pattern_count': len(applicable_patterns),
        'confidence_score': avg_confidence,
        'recommendation': 'HIGH CONVICTION' if avg_confidence >= 9.0 else
                         'MODERATE CONVICTION' if avg_confidence >= 7.0 else
                         'LOW CONVICTION'
    }
