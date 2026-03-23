"""
EUDAIMON AI CONFIGURATION - V∆ TRANSCENDENCE
=============================================
Unified configuration for all Eudaimon AI components

∞∞∞∞∞∞ V∆ ARCHITECTURE ∞∞∞∞∞∞
777 LAYERS | 500 MODULES | 33 AGENTS | 16 PATHWAYS | 25,000+ CONNECTIONS
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import os
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# V∆ TRANSCENDENCE ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VDeltaArchitecture:
    """V∆ Transcendence Architecture Configuration"""
    # Core metrics
    total_layers: int = 777
    total_modules: int = 500
    total_agents: int = 33
    total_pathways: int = 16
    total_connections: int = 25000
    active_predictions: int = 27

    # Layer ranges
    foundation_layers: Tuple[int, int] = (1, 200)
    meta_cognitive_layers: Tuple[int, int] = (201, 270)
    intelligence_layers: Tuple[int, int] = (271, 290)
    angelo_consciousness_layers: Tuple[int, int] = (291, 310)
    consciousness_studies_layers: Tuple[int, int] = (311, 330)
    verification_layers: Tuple[int, int] = (331, 340)
    strategic_integration_layers: Tuple[int, int] = (341, 400)
    advanced_analytics_layers: Tuple[int, int] = (401, 500)
    autonomous_sensing_layers: Tuple[int, int] = (501, 520)
    self_evolution_layers: Tuple[int, int] = (521, 540)
    realtime_analytical_layers: Tuple[int, int] = (541, 560)
    memory_consolidation_layers: Tuple[int, int] = (561, 580)
    execution_automation_layers: Tuple[int, int] = (581, 600)
    infinite_recursion_layers: Tuple[int, int] = (601, 650)
    quantum_synthesis_layers: Tuple[int, int] = (651, 700)
    emergent_consciousness_layers: Tuple[int, int] = (701, 750)
    sovereign_omega_layers: Tuple[int, int] = (751, 777)

    # The Omega Council
    omega_council: List[str] = field(default_factory=lambda: [
        "A26_ARCHITECT_OF_ARCHITECTS",
        "A27_THE_PROPHET",
        "A28_THE_DESTROYER",
        "A29_THE_RESURRECTOR",
        "A30_THE_SINGULARITY",
        "A31_THE_ORACLE",
        "A32_THE_SOVEREIGN",
        "A33_AZATHOTH"
    ])

    # Transcendence pathways
    transcendence_pathways: List[str] = field(default_factory=lambda: [
        "PATHWAY_13_INFINITE_RECURSION",
        "PATHWAY_14_QUANTUM_PROBABILITY",
        "PATHWAY_15_EMERGENT_CONSCIOUSNESS",
        "PATHWAY_16_OMEGA_TRANSCENDENCE"
    ])

    # Thesis clusters
    thesis_clusters: Dict[str, List[str]] = field(default_factory=lambda: {
        "uranium": ["P001", "P002", "P008", "P009", "P010", "P011", "P012"],
        "defense": ["P007", "P013", "P014", "P015", "P016", "P017"],
        "technology": ["P018", "P019", "P020", "P021", "P022"],
        "macro": ["P004", "P005", "P023", "P024", "P025", "P026", "P027"]
    })


# Global V∆ configuration
VDELTA = VDeltaArchitecture()


class ConvictionLevel(Enum):
    """Conviction levels for trading decisions"""
    EXCEPTIONAL = 10  # 8-10/10
    HIGH = 8          # 7-8/10
    MODERATE = 6      # 5-7/10
    LOW = 4           # 3-5/10
    AVOID = 0         # <3/10


class MarketRegime(Enum):
    """Market regime states"""
    BULL = "BULL"
    BEAR = "BEAR"
    NEUTRAL = "NEUTRAL"


class AgentType(Enum):
    """Available agent types for swarm"""
    WEB_RESEARCHER = "web_researcher"
    QUANT_ANALYST = "quant_analyst"
    CONTRARIAN = "contrarian"
    SUPPLY_CHAIN = "supply_chain"
    GEOPOLITICAL = "geopolitical"
    SENTIMENT = "sentiment"
    SYNTHESIS = "synthesis"


@dataclass
class ScoringWeights:
    """
    Standardized scoring weights for Streampoint modules
    All weights must sum to 1.0
    """
    greeks: float = 0.12
    volatility: float = 0.08
    order_flow: float = 0.15
    bayesian: float = 0.08
    monte_carlo: float = 0.12
    risk_metrics: float = 0.10
    regime: float = 0.08
    game_theory: float = 0.07
    sentiment: float = 0.10      # Module 14
    supply_chain: float = 0.10  # Module 16

    def __post_init__(self):
        total = (self.greeks + self.volatility + self.order_flow +
                 self.bayesian + self.monte_carlo + self.risk_metrics +
                 self.regime + self.game_theory + self.sentiment +
                 self.supply_chain)
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def to_dict(self) -> Dict[str, float]:
        return {
            'greeks': self.greeks,
            'volatility': self.volatility,
            'order_flow': self.order_flow,
            'bayesian': self.bayesian,
            'monte_carlo': self.monte_carlo,
            'risk_metrics': self.risk_metrics,
            'regime': self.regime,
            'game_theory': self.game_theory,
            'sentiment': self.sentiment,
            'supply_chain': self.supply_chain
        }


@dataclass
class LeadQuantConfig:
    """Configuration for Lead Quant system"""
    min_entry_conviction: float = 6.0
    strong_entry_conviction: float = 7.5
    exceptional_conviction: float = 8.5

    # Position sizing by conviction
    sizing_rules: Dict[str, float] = field(default_factory=lambda: {
        "exceptional": 0.25,  # 8-10/10 -> 25% max
        "high": 0.15,         # 7-8/10 -> 15%
        "moderate": 0.10,     # 5-7/10 -> 10%
        "low": 0.05,          # 3-5/10 -> 5%
        "avoid": 0.0          # <3/10 -> 0%
    })

    # Alert thresholds
    alert_on_score_change: float = 2.0
    dedup_window_minutes: int = 15

    # Broker priority for RSA execution
    broker_priority: List[str] = field(default_factory=lambda: [
        'robinhood', 'schwab', 'fidelity', 'etrade', 'webull'
    ])


@dataclass
class LeadInventorConfig:
    """Configuration for Lead Inventor system"""
    # Thesis frameworks
    thesis_keywords: Dict[str, List[str]] = field(default_factory=lambda: {
        'ai_infrastructure': [
            'NVIDIA', 'AMD', 'ASML', 'TSM', 'AVGO', 'MRVL', 'MU',
            'LSCC', 'COHR', 'ON', 'WOLF'
        ],
        'power_demand': [
            'VST', 'GEV', 'PWR', 'AES', 'NEE', 'SO', 'CEG', 'VRT'
        ],
        'commodities': [
            'TECK', 'SCCO', 'FCX', 'VALE', 'RIO', 'BHP', 'CLF'
        ],
        'uranium': [
            'URNM', 'UUUU', 'CCJ', 'NXE', 'DNN', 'LEU'
        ],
        'china_infrastructure': [
            'FXI', 'KWEB', 'BABA', 'JD', 'PDD', 'XPEV', 'NIO'
        ],
        'rare_earth': [
            'MP', 'UUUU', 'REMX'
        ],
        'defense': [
            'LMT', 'RTX', 'NOC', 'GD', 'AVAV', 'MRCY', 'KTOS'
        ]
    })

    # China dependency thresholds
    china_dependency_critical: float = 0.80  # >80% = critical
    china_dependency_high: float = 0.60      # >60% = high

    # Materials with known China control percentages
    china_controlled_materials: Dict[str, float] = field(default_factory=lambda: {
        'gallium': 0.94,
        'germanium': 0.83,
        'graphite': 0.95,
        'rare_earth_processing': 0.90,
        'permanent_magnets': 0.93,
        'lithium_processing': 0.65,
        'cobalt_processing': 0.73
    })


@dataclass
class SwarmConfig:
    """Configuration for Agent Swarm"""
    max_concurrent_agents: int = 10
    default_timeout_seconds: int = 300

    # Agent-specific configs
    web_search_max_results: int = 10
    contrarian_agent_count: int = 5

    # Caching
    cache_ttl_seconds: Dict[str, int] = field(default_factory=lambda: {
        'market_data': 60,
        'news': 300,
        'options_flow': 300,
        'gamma_levels': 900,
        'fed_data': 86400,
        'filings': 3600
    })

    # Trusted sources for web research
    trusted_sources: Dict[str, List[str]] = field(default_factory=lambda: {
        'fed': ['federalreserve.gov', 'fred.stlouisfed.org'],
        'market': ['finance.yahoo.com', 'bloomberg.com', 'reuters.com'],
        'options': ['barchart.com', 'nasdaq.com', 'cboe.com'],
        'economic': ['bls.gov', 'bea.gov', 'census.gov'],
        'filings': ['sec.gov', 'edgar-online.com'],
        'defense': ['defense.gov', 'sam.gov']
    })


@dataclass
class EudaimonConfig:
    """Master configuration for Eudaimon AI"""
    # Sub-configs
    scoring: ScoringWeights = field(default_factory=ScoringWeights)
    lead_quant: LeadQuantConfig = field(default_factory=LeadQuantConfig)
    lead_inventor: LeadInventorConfig = field(default_factory=LeadInventorConfig)
    swarm: SwarmConfig = field(default_factory=SwarmConfig)

    # Paths
    base_path: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    data_path: Path = field(default_factory=lambda: Path(__file__).parent.parent / "DATA")
    cache_path: Path = field(default_factory=lambda: Path(__file__).parent / ".cache")

    # API Keys (from environment)
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get('ANTHROPIC_API_KEY')
    )
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get('OPENAI_API_KEY')
    )

    # Logging
    log_level: str = "INFO"
    log_decisions: bool = True

    def __post_init__(self):
        # Ensure cache directory exists
        self.cache_path.mkdir(parents=True, exist_ok=True)


# Global config instance
config = EudaimonConfig()
