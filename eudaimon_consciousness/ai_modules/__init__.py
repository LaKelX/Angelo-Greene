"""
EUDAIMON AI
===========
Unified AI Research & Trading Intelligence Platform

KEY DIFFERENTIATOR: Full Game Theory & Quant Engine
- Nash Equilibrium for optimal entry timing
- Kelly Criterion for position sizing
- Monte Carlo simulations (GBM + Jump Diffusion)
- CVaR, Sharpe, Sortino risk metrics
- Regime detection with GMM

Consolidates:
- Streampoint Research Engine (16+ modules)
- Lead Quant (conviction scoring, signals, execution)
- Lead Inventor (supply chain, bottleneck analysis)
- Agent Swarm (parallel research minions)
- Game Theory & Quant Engine (THE KEY FEATURE)

Part of the Eudaimon Ecosystem:
- Eudaimon Capitol: RSA trading, client brokerages, LEAPS strategies
- Eudaimon Energy: Texas ERCOT demand response aggregation
- Eudaimon AI: Intelligence layer (this package)

Usage:
    from eudaimon_ai import EudaimonAI

    ai = EudaimonAI()

    # Basic analysis
    result = ai.analyze("URNM", thesis="uranium supercycle")

    # FULL QUANT ANALYSIS WITH GAME THEORY (THE KEY FEATURE)
    quant = ai.quant_analysis("AAPL", target_price=200, stop_price=170)
    print(f"Win Probability: {quant['key_metrics']['win_probability']}")
    print(f"Optimal Entry: {quant['key_metrics']['optimal_entry']}")
    print(f"Kelly Size: {quant['key_metrics']['kelly_position']*100}%")

    # Direct quant engine access
    from eudaimon_ai.quant import GameTheoryAnalyzer, MonteCarloEngine

CLI:
    eudaimon quant score AAPL --thesis "AI infrastructure"
    eudaimon inventor research --topic "SiC semiconductors"
    eudaimon streampoint 360 SPY QQQ
    eudaimon swarm spawn --task "copper supply chain analysis"
"""

__version__ = "1.0.0"
__author__ = "Diego M. Gonzalez"
__email__ = "DiegoGonzalez@eudaimonus.com"

from .core.eudaimon import EudaimonAI
from .core.lead_quant import LeadQuant
from .core.lead_inventor import LeadInventor
from .agents.swarm import EudaimonSwarm

# Export Portfolio Module (Holdings Tracker)
from .portfolio import (
    HoldingsTracker,
    Account,
    Position,
    AccountType,
    AssetType,
    get_tracker
)

# Export Quant Engine components (THE KEY FEATURES)
from .quant.quant_engine import (
    GameTheoryAnalyzer,
    MonteCarloEngine,
    RiskAnalyzer,
    PortfolioOptimizer,
    RegimeDetector,
    TechnicalIndicators,
    run_comprehensive_analysis
)
from .quant.game_theory import (
    MarketGameTheory,
    run_game_theory_analysis
)

# Export Uncertainty Quantification Module
from .quant.uncertainty_quantification import (
    UncertaintyEngine,
    UncertaintyEstimate,
    TradingRecommendation,
    TradingAction,
    UncertaintyType,
    SplitConformalPredictor,
    AdaptiveConformalInference,
    DeepEnsemble,
    TemperatureScaling,
    create_uncertainty_engine,
    quick_uncertainty_analysis,
)

# Conditional PyTorch components
try:
    from .quant.uncertainty_quantification import (
        BayesianLinear,
        LastLayerBayesianNetwork,
        DualUncertaintyNetwork,
        MCDropoutNetwork,
        QuantileRegressionNetwork,
        NonCrossingQuantileNetwork,
        QRDQNValueHead,
    )
    _UQ_TORCH_AVAILABLE = True
except ImportError:
    _UQ_TORCH_AVAILABLE = False

# Export Causal Inference and Discovery Module
from .causal_inference import (
    CausalInferenceEngine,
    NOTEARS,
    DYNOTEARS,
    NeuralGrangerCausality,
    TransferEntropy,
    CounterfactualAnalyzer,
    CATEEstimator,
    CausalRepresentationLearner,
    CausalGraph,
    CounterfactualResult,
    TreatmentEffect,
    generate_synthetic_dag_data,
    quick_causal_test
)

# Export RL Trading Agents (Reinforcement Learning Module)
from .rl_trading_agents import (
    RLTradingSystem,
    PPOPortfolioManager,
    DQNRiskManager,
    MultiAgentEnsemble,
    WorldModelRL,
    ConservativeQLearning,
    MomentumAgent,
    MeanReversionAgent,
    VolatilityArbitrageAgent,
    ExperienceReplayBuffer,
    RewardShaper,
    MarketState,
    Experience,
    RewardMetrics,
    MarketRegime as RLMarketRegime,
    RiskAction,
    create_market_state,
    compute_reward_metrics
)

# Export Attention Mechanisms for Financial Time Series
from .attention_mechanisms import (
    AttentionTimeSeriesPredictor,
    MultiHeadAttention,
    MultiHorizonAttention,
    CrossAssetAttention,
    TemporalPatternAttention,
    HierarchicalAttention,
    SparseAttention,
    EventAttentionLayer,
    create_attention_predictor,
    TimeHorizon,
    MarketRegime,
    AttentionConfig
)

# Export Graph Neural Networks for Market Analysis
from .quant.graph_neural_networks import (
    # Main Orchestrator
    GraphNeuralMarketAnalyzer,
    # Graph Building
    MarketGraphBuilder,
    MarketGraph,
    # GNN Models
    TemporalGraphNetwork,
    GraphAttentionNetwork,
    HeterogeneousGraphNetwork,
    RelationalGCN,
    # Analysis Modules
    ShockPropagationPredictor,
    LeadingIndicatorIdentifier,
    SectorRotationDetector,
    # Data Classes
    GraphNode,
    GraphEdge,
    NodeType,
    EdgeType,
    ShockPropagationResult,
    LeadingIndicatorResult,
    SectorRotationSignal,
    # Convenience Functions
    create_market_graph_from_prices,
    quick_shock_analysis,
    quick_leader_analysis,
)

# Export Transformer Models for Financial Time Series
from .transformer_models import (
    TransformerPriceEngine,
    TransformerConfig,
    PredictionResult,
    TimeHorizon as TransformerTimeHorizon,
    SectorInfo,
    create_engine,
    quick_predict,
)

# Export Swarm Coordination Module
from .swarm_coordination import (
    SwarmCoordinator,
    QMIXCoordinator,
    PSOAllocator,
    ACORouter,
    ByzantineFaultTolerantConsensus,
    TarMACCommunication,
    HeterogeneousAgentTeam,
    MeanFieldMARLCoordinator,
    InventoryManagementSwarm,
    Signal,
    ConsensusResult,
    AllocationResult,
    RoutingResult,
    AgentRole,
    DecisionType,
    RegimeType as SwarmRegimeType,
    TimeHorizon as SwarmTimeHorizon,
    create_default_swarm,
    run_swarm_analysis,
)

__all__ = [
    # Main Classes
    "EudaimonAI",
    "LeadQuant",
    "LeadInventor",
    "EudaimonSwarm",
    # Quant Engine (THE KEY FEATURES)
    "GameTheoryAnalyzer",
    "MonteCarloEngine",
    "RiskAnalyzer",
    "PortfolioOptimizer",
    "RegimeDetector",
    "TechnicalIndicators",
    "MarketGameTheory",
    # Functions
    "run_comprehensive_analysis",
    "run_game_theory_analysis",
    # Uncertainty Quantification
    "UncertaintyEngine",
    "UncertaintyEstimate",
    "TradingRecommendation",
    "TradingAction",
    "UncertaintyType",
    "SplitConformalPredictor",
    "AdaptiveConformalInference",
    "DeepEnsemble",
    "TemperatureScaling",
    "create_uncertainty_engine",
    "quick_uncertainty_analysis",
    # Causal Inference and Discovery
    "CausalInferenceEngine",
    "NOTEARS",
    "DYNOTEARS",
    "NeuralGrangerCausality",
    "TransferEntropy",
    "CounterfactualAnalyzer",
    "CATEEstimator",
    "CausalRepresentationLearner",
    "CausalGraph",
    "CounterfactualResult",
    "TreatmentEffect",
    "generate_synthetic_dag_data",
    "quick_causal_test",
    # Attention Mechanisms
    "AttentionTimeSeriesPredictor",
    "MultiHeadAttention",
    "MultiHorizonAttention",
    "CrossAssetAttention",
    "TemporalPatternAttention",
    "HierarchicalAttention",
    "SparseAttention",
    "EventAttentionLayer",
    "create_attention_predictor",
    "TimeHorizon",
    "MarketRegime",
    "AttentionConfig",
    # RL Trading Agents
    "RLTradingSystem",
    "PPOPortfolioManager",
    "DQNRiskManager",
    "MultiAgentEnsemble",
    "WorldModelRL",
    "ConservativeQLearning",
    "MomentumAgent",
    "MeanReversionAgent",
    "VolatilityArbitrageAgent",
    "ExperienceReplayBuffer",
    "RewardShaper",
    "MarketState",
    "Experience",
    "RewardMetrics",
    "RLMarketRegime",
    "RiskAction",
    "create_market_state",
    "compute_reward_metrics",
    # Graph Neural Networks
    "GraphNeuralMarketAnalyzer",
    "MarketGraphBuilder",
    "MarketGraph",
    "TemporalGraphNetwork",
    "GraphAttentionNetwork",
    "HeterogeneousGraphNetwork",
    "RelationalGCN",
    "ShockPropagationPredictor",
    "LeadingIndicatorIdentifier",
    "SectorRotationDetector",
    "GraphNode",
    "GraphEdge",
    "NodeType",
    "EdgeType",
    "ShockPropagationResult",
    "LeadingIndicatorResult",
    "SectorRotationSignal",
    "create_market_graph_from_prices",
    "quick_shock_analysis",
    "quick_leader_analysis",
    # Transformer Models
    "TransformerPriceEngine",
    "TransformerConfig",
    "PredictionResult",
    "create_engine",
    "quick_predict",
    # Swarm Coordination
    "SwarmCoordinator",
    "QMIXCoordinator",
    "PSOAllocator",
    "ACORouter",
    "ByzantineFaultTolerantConsensus",
    "TarMACCommunication",
    "HeterogeneousAgentTeam",
    "MeanFieldMARLCoordinator",
    "InventoryManagementSwarm",
    "Signal",
    "ConsensusResult",
    "AllocationResult",
    "RoutingResult",
    "AgentRole",
    "DecisionType",
    "create_default_swarm",
    "run_swarm_analysis",
]
