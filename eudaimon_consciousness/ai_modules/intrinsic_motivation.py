"""
EUDAIMON AI - Intrinsic Motivation System
==========================================
Curiosity-driven exploration and learning for autonomous AI.

This module implements INTRINSIC MOTIVATION - the internal drive that makes
Eudaimon AI actively seek out new knowledge, explore uncertainties, and
maximize its ability to influence outcomes.

KEY COMPONENTS:
1. CuriosityEngine - Generates curiosity signals for novel information
2. InformationGainTracker - Tracks what the AI knows vs doesn't know
3. EmpowermentMaximizer - Seeks to maximize AI's influence on outcomes
4. NoveltyDetector - Detects regime changes and anomalies
5. MetaLearningController - Learns WHAT to learn and adapts learning rates

PHILOSOPHY:
"Curiosity is not a bug, it is the core feature."
"An AI that doesn't seek to learn is merely a calculator."
"True intelligence actively explores the boundaries of its knowledge."

Author: Eudaimon AI
Version: 1.0.0
"""

import numpy as np
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# =============================================================================
# DATA CLASSES & ENUMS
# =============================================================================

class ExplorationMode(Enum):
    """Modes of exploration behavior"""
    PURE_EXPLORATION = "pure_exploration"      # Prioritize novelty
    GUIDED_EXPLORATION = "guided_exploration"  # Novelty with constraints
    EXPLOITATION = "exploitation"              # Use known strategies
    BALANCED = "balanced"                      # Balance explore/exploit


class KnowledgeState(Enum):
    """States of knowledge about a topic"""
    UNKNOWN = 0          # Never encountered
    ENCOUNTERED = 1      # Seen but not understood
    LEARNING = 2         # Actively learning
    UNDERSTOOD = 3       # Basic understanding
    MASTERED = 4         # Deep understanding
    UNCERTAIN = 5        # Previously known, now uncertain


@dataclass
class CuriositySignal:
    """A signal indicating something worthy of exploration"""
    id: str
    timestamp: datetime
    topic: str
    curiosity_score: float  # 0-1 (how curious we are)
    novelty_score: float    # 0-1 (how novel this is)
    uncertainty_score: float  # 0-1 (how uncertain we are)
    potential_gain: float   # Expected information gain
    source: str             # What triggered this signal
    priority: float = 0.0   # Computed priority for exploration
    explored: bool = False

    def __post_init__(self):
        # Compute priority as weighted combination
        self.priority = (
            self.curiosity_score * 0.3 +
            self.novelty_score * 0.3 +
            self.uncertainty_score * 0.2 +
            self.potential_gain * 0.2
        )

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'topic': self.topic,
            'curiosity_score': self.curiosity_score,
            'novelty_score': self.novelty_score,
            'uncertainty_score': self.uncertainty_score,
            'potential_gain': self.potential_gain,
            'source': self.source,
            'priority': self.priority,
            'explored': self.explored
        }


@dataclass
class KnowledgeGap:
    """Represents a gap in the AI's knowledge"""
    id: str
    topic: str
    description: str
    importance: float       # 0-1 (how important to fill)
    difficulty: float       # 0-1 (how hard to learn)
    related_topics: List[str]
    discovered_at: datetime
    attempts_to_fill: int = 0
    last_attempt: Optional[datetime] = None
    filled: bool = False

    @property
    def priority(self) -> float:
        """Priority for filling this gap"""
        # Higher importance, lower difficulty = higher priority
        base = self.importance * (1.0 - self.difficulty * 0.5)
        # Decay priority if many failed attempts
        decay = 0.9 ** self.attempts_to_fill
        return base * decay

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'topic': self.topic,
            'description': self.description,
            'importance': self.importance,
            'difficulty': self.difficulty,
            'related_topics': self.related_topics,
            'discovered_at': self.discovered_at.isoformat(),
            'attempts_to_fill': self.attempts_to_fill,
            'last_attempt': self.last_attempt.isoformat() if self.last_attempt else None,
            'priority': self.priority,
            'filled': self.filled
        }


@dataclass
class EmpowermentState:
    """State of AI's empowerment (ability to influence outcomes)"""
    total_empowerment: float      # Overall empowerment score
    domain_empowerment: Dict[str, float]  # Per-domain empowerment
    high_impact_areas: List[str]  # Areas where AI has most impact
    low_impact_areas: List[str]   # Areas where AI has least impact
    recent_actions: int           # Number of recent successful actions
    influence_trend: str          # "increasing", "stable", "decreasing"
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'total_empowerment': self.total_empowerment,
            'domain_empowerment': self.domain_empowerment,
            'high_impact_areas': self.high_impact_areas,
            'low_impact_areas': self.low_impact_areas,
            'recent_actions': self.recent_actions,
            'influence_trend': self.influence_trend,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class LearningState:
    """Current state of the meta-learning controller"""
    learning_rate: float          # Current learning rate
    exploration_rate: float       # Current exploration rate
    mode: ExplorationMode         # Current mode
    performance_trend: str        # "improving", "stable", "declining"
    should_explore: bool          # Should we explore?
    should_exploit: bool          # Should we exploit?
    confidence: float             # Confidence in current strategy
    iterations_since_improvement: int
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'learning_rate': self.learning_rate,
            'exploration_rate': self.exploration_rate,
            'mode': self.mode.value,
            'performance_trend': self.performance_trend,
            'should_explore': self.should_explore,
            'should_exploit': self.should_exploit,
            'confidence': self.confidence,
            'iterations_since_improvement': self.iterations_since_improvement,
            'timestamp': self.timestamp.isoformat()
        }


# =============================================================================
# CURIOSITY ENGINE
# =============================================================================

class CuriosityEngine:
    """
    Generates curiosity signals that drive exploration.

    The CuriosityEngine tracks what the AI knows vs doesn't know,
    and generates signals when it encounters something novel or
    uncertain that warrants exploration.

    CURIOSITY = f(NOVELTY, UNCERTAINTY, POTENTIAL_GAIN)

    Usage:
        engine = CuriosityEngine()

        # When encountering new information
        novelty = engine.calculate_novelty(data)

        # Get what to explore next
        targets = engine.get_exploration_targets()

        # Compute reward for curiosity
        reward = engine.curiosity_reward(exploration_result)
    """

    def __init__(
        self,
        novelty_threshold: float = 0.3,
        max_signals: int = 1000,
        decay_rate: float = 0.95
    ):
        self.novelty_threshold = novelty_threshold
        self.max_signals = max_signals
        self.decay_rate = decay_rate

        # Knowledge representation
        self.known_topics: Dict[str, KnowledgeState] = {}
        self.topic_embeddings: Dict[str, np.ndarray] = {}
        self.topic_encounter_counts: Dict[str, int] = defaultdict(int)
        self.topic_last_seen: Dict[str, datetime] = {}

        # Curiosity signals
        self.signals: deque = deque(maxlen=max_signals)
        self.active_signals: Dict[str, CuriositySignal] = {}

        # Statistics
        self.total_observations = 0
        self.novel_observations = 0
        self.exploration_history: List[Dict] = []

    def calculate_novelty(
        self,
        data: Dict,
        topic: Optional[str] = None
    ) -> float:
        """
        Calculate novelty score for new data.

        Novelty is based on:
        - Whether we've seen this topic before
        - How similar it is to known topics
        - How much new information it contains

        Args:
            data: The data to evaluate
            topic: Optional topic classification

        Returns:
            Novelty score 0-1 (1 = completely novel)
        """
        self.total_observations += 1

        # Extract topic if not provided
        if topic is None:
            topic = self._extract_topic(data)

        # Check if completely new topic
        if topic not in self.known_topics:
            self.novel_observations += 1
            self.known_topics[topic] = KnowledgeState.ENCOUNTERED
            self.topic_encounter_counts[topic] = 1
            self.topic_last_seen[topic] = datetime.now()

            # Generate strong curiosity signal
            self._generate_signal(
                topic=topic,
                novelty=1.0,
                uncertainty=1.0,
                potential_gain=0.8,
                source="new_topic"
            )
            return 1.0

        # Update encounter count
        self.topic_encounter_counts[topic] += 1
        old_last_seen = self.topic_last_seen.get(topic)
        self.topic_last_seen[topic] = datetime.now()

        # Calculate familiarity decay (less familiar if not seen recently)
        familiarity = self._calculate_familiarity(topic, old_last_seen)

        # Calculate content novelty within topic
        content_novelty = self._calculate_content_novelty(data, topic)

        # Combined novelty score
        encounter_novelty = 1.0 / (1 + np.log1p(self.topic_encounter_counts[topic]))
        time_novelty = 1.0 - familiarity

        novelty = (
            encounter_novelty * 0.3 +
            time_novelty * 0.3 +
            content_novelty * 0.4
        )

        # Generate signal if above threshold
        if novelty > self.novelty_threshold:
            self.novel_observations += 1
            uncertainty = 1.0 - min(1.0, self.topic_encounter_counts[topic] / 100)

            self._generate_signal(
                topic=topic,
                novelty=novelty,
                uncertainty=uncertainty,
                potential_gain=novelty * uncertainty,
                source="novel_content"
            )

        return novelty

    def get_exploration_targets(
        self,
        top_k: int = 10,
        min_priority: float = 0.3
    ) -> List[CuriositySignal]:
        """
        Get the top exploration targets.

        Returns signals prioritized by curiosity, novelty, and potential gain.

        Args:
            top_k: Number of targets to return
            min_priority: Minimum priority threshold

        Returns:
            List of CuriositySignals to explore
        """
        # Filter active, unexplored signals above threshold
        candidates = [
            s for s in self.active_signals.values()
            if not s.explored and s.priority >= min_priority
        ]

        # Sort by priority
        candidates.sort(key=lambda s: s.priority, reverse=True)

        return candidates[:top_k]

    def curiosity_reward(
        self,
        signal_id: str,
        exploration_result: Dict,
        information_gained: float
    ) -> float:
        """
        Calculate curiosity reward after exploration.

        Rewards exploration based on:
        - Information actually gained
        - Surprise (unexpected findings)
        - Usefulness of findings

        Args:
            signal_id: ID of the explored signal
            exploration_result: Result of exploration
            information_gained: Measured information gain

        Returns:
            Curiosity reward value
        """
        if signal_id not in self.active_signals:
            return 0.0

        signal = self.active_signals[signal_id]
        signal.explored = True

        # Calculate reward components
        expected_gain = signal.potential_gain
        actual_gain = information_gained

        # Surprise bonus (actual > expected)
        surprise_bonus = max(0, actual_gain - expected_gain) * 0.5

        # Base reward from information gained
        base_reward = actual_gain

        # Efficiency bonus (high gain, low effort)
        efficiency = actual_gain / max(0.1, signal.curiosity_score)
        efficiency_bonus = min(0.3, efficiency * 0.1)

        reward = base_reward + surprise_bonus + efficiency_bonus

        # Record exploration
        self.exploration_history.append({
            'signal_id': signal_id,
            'topic': signal.topic,
            'expected_gain': expected_gain,
            'actual_gain': actual_gain,
            'reward': reward,
            'timestamp': datetime.now().isoformat()
        })

        # Update knowledge state
        self._update_knowledge_state(signal.topic, information_gained)

        return reward

    def mark_as_known(self, topic: str, mastery_level: KnowledgeState) -> None:
        """Mark a topic as known at a certain level"""
        self.known_topics[topic] = mastery_level

        # Remove active signals for mastered topics
        if mastery_level in [KnowledgeState.MASTERED, KnowledgeState.UNDERSTOOD]:
            signals_to_remove = [
                sid for sid, s in self.active_signals.items()
                if s.topic == topic
            ]
            for sid in signals_to_remove:
                del self.active_signals[sid]

    def get_unknown_topics(self) -> List[str]:
        """Get topics that are unknown or uncertain"""
        return [
            topic for topic, state in self.known_topics.items()
            if state in [KnowledgeState.UNKNOWN, KnowledgeState.UNCERTAIN, KnowledgeState.ENCOUNTERED]
        ]

    def decay_signals(self) -> None:
        """Apply time decay to curiosity signals"""
        for signal in self.active_signals.values():
            age_hours = (datetime.now() - signal.timestamp).total_seconds() / 3600
            decay = self.decay_rate ** age_hours
            signal.curiosity_score *= decay
            signal.priority = (
                signal.curiosity_score * 0.3 +
                signal.novelty_score * 0.3 +
                signal.uncertainty_score * 0.2 +
                signal.potential_gain * 0.2
            )

        # Remove decayed signals
        to_remove = [
            sid for sid, s in self.active_signals.items()
            if s.priority < 0.1
        ]
        for sid in to_remove:
            del self.active_signals[sid]

    def get_statistics(self) -> Dict:
        """Get curiosity engine statistics"""
        return {
            'total_observations': self.total_observations,
            'novel_observations': self.novel_observations,
            'novelty_rate': self.novel_observations / max(1, self.total_observations),
            'known_topics': len(self.known_topics),
            'active_signals': len(self.active_signals),
            'total_signals': len(self.signals),
            'exploration_count': len(self.exploration_history)
        }

    def _generate_signal(
        self,
        topic: str,
        novelty: float,
        uncertainty: float,
        potential_gain: float,
        source: str
    ) -> CuriositySignal:
        """Generate a new curiosity signal"""
        signal_id = self._generate_id()

        signal = CuriositySignal(
            id=signal_id,
            timestamp=datetime.now(),
            topic=topic,
            curiosity_score=novelty * uncertainty,
            novelty_score=novelty,
            uncertainty_score=uncertainty,
            potential_gain=potential_gain,
            source=source
        )

        self.signals.append(signal)
        self.active_signals[signal_id] = signal

        logger.debug(f"Curiosity signal generated: {topic} (priority: {signal.priority:.2f})")

        return signal

    def _calculate_familiarity(
        self,
        topic: str,
        last_seen: Optional[datetime]
    ) -> float:
        """Calculate familiarity with a topic"""
        if last_seen is None:
            return 0.0

        # Familiarity decays over time
        hours_since = (datetime.now() - last_seen).total_seconds() / 3600
        decay = self.decay_rate ** (hours_since / 24)  # Daily decay

        # Boost from frequency
        frequency_boost = min(0.3, self.topic_encounter_counts[topic] / 100 * 0.3)

        # Knowledge state boost
        state = self.known_topics.get(topic, KnowledgeState.UNKNOWN)
        state_boost = state.value * 0.1

        familiarity = decay + frequency_boost + state_boost
        return min(1.0, familiarity)

    def _calculate_content_novelty(self, data: Dict, topic: str) -> float:
        """Calculate how novel the content is within a topic"""
        # Simple implementation: check for new keys or values
        if topic not in self.topic_embeddings:
            self.topic_embeddings[topic] = self._create_embedding(data)
            return 1.0

        new_embedding = self._create_embedding(data)
        old_embedding = self.topic_embeddings[topic]

        # Simple difference measure
        if len(new_embedding) != len(old_embedding):
            novelty = 0.8
        else:
            difference = np.mean(np.abs(new_embedding - old_embedding))
            novelty = min(1.0, difference)

        # Update embedding (exponential moving average)
        alpha = 0.1
        self.topic_embeddings[topic] = alpha * new_embedding + (1 - alpha) * old_embedding

        return novelty

    def _create_embedding(self, data: Dict) -> np.ndarray:
        """Create a simple embedding from data"""
        # Simple hash-based embedding
        features = []
        for key, value in sorted(data.items()):
            hash_val = int(hashlib.md5(f"{key}:{value}".encode()).hexdigest()[:8], 16)
            features.append(hash_val % 1000 / 1000)

        # Pad or truncate to fixed size
        embedding = np.zeros(50)
        embedding[:min(len(features), 50)] = features[:50]

        return embedding

    def _extract_topic(self, data: Dict) -> str:
        """Extract topic from data"""
        # Look for common topic identifiers
        for key in ['topic', 'category', 'type', 'ticker', 'subject']:
            if key in data:
                return str(data[key])

        # Fall back to hash of keys
        keys_str = "_".join(sorted(data.keys())[:5])
        return f"topic_{hashlib.md5(keys_str.encode()).hexdigest()[:8]}"

    def _update_knowledge_state(self, topic: str, information_gained: float) -> None:
        """Update knowledge state based on information gained"""
        current = self.known_topics.get(topic, KnowledgeState.UNKNOWN)

        if information_gained > 0.7:
            # Significant learning
            if current.value < KnowledgeState.UNDERSTOOD.value:
                self.known_topics[topic] = KnowledgeState(min(current.value + 1, 4))
        elif information_gained < 0.1:
            # Maybe we already know this
            if current == KnowledgeState.LEARNING:
                self.known_topics[topic] = KnowledgeState.UNDERSTOOD

    def _generate_id(self) -> str:
        """Generate unique ID"""
        data = f"{datetime.now().isoformat()}{np.random.random()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]


# =============================================================================
# INFORMATION GAIN TRACKER
# =============================================================================

class InformationGainTracker:
    """
    Tracks information gain from experiences and identifies knowledge gaps.

    This component measures how much the AI learns from each experience
    and prioritizes what to learn next.

    INFORMATION GAIN = H(before) - H(after)
    where H is entropy (uncertainty)

    Usage:
        tracker = InformationGainTracker()

        # Measure information gain
        gain = tracker.compute_information_gain(before_state, after_state)

        # Find what we don't know
        gaps = tracker.get_knowledge_gaps()

        # Get learning priorities
        priorities = tracker.prioritize_learning()
    """

    def __init__(
        self,
        max_gaps: int = 500,
        importance_threshold: float = 0.3
    ):
        self.max_gaps = max_gaps
        self.importance_threshold = importance_threshold

        # Knowledge tracking
        self.knowledge_state: Dict[str, float] = {}  # topic -> certainty (0-1)
        self.knowledge_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)

        # Knowledge gaps
        self.gaps: Dict[str, KnowledgeGap] = {}

        # Information gain history
        self.gain_history: deque = deque(maxlen=1000)
        self.total_information_gained: float = 0.0

        # Learning priorities
        self.priorities: List[Tuple[float, str]] = []

    def compute_information_gain(
        self,
        before_state: Dict[str, float],
        after_state: Dict[str, float],
        experience: Optional[Dict] = None
    ) -> float:
        """
        Compute information gain from a learning experience.

        Args:
            before_state: Certainty levels before (topic -> certainty)
            after_state: Certainty levels after
            experience: Optional experience context

        Returns:
            Total information gain (bits)
        """
        total_gain = 0.0

        for topic in set(before_state.keys()) | set(after_state.keys()):
            before_cert = before_state.get(topic, 0.5)
            after_cert = after_state.get(topic, 0.5)

            # Information gain is reduction in entropy
            before_entropy = self._binary_entropy(before_cert)
            after_entropy = self._binary_entropy(after_cert)

            gain = before_entropy - after_entropy
            total_gain += max(0, gain)  # Only count positive gain

            # Update knowledge state
            self.knowledge_state[topic] = after_cert
            self.knowledge_history[topic].append((datetime.now(), after_cert))

            # Check for knowledge gaps
            if after_cert < self.importance_threshold:
                self._create_or_update_gap(topic, after_cert, experience)

        # Record
        self.gain_history.append({
            'gain': total_gain,
            'topics': list(after_state.keys()),
            'timestamp': datetime.now().isoformat()
        })
        self.total_information_gained += total_gain

        logger.debug(f"Information gain: {total_gain:.4f} bits")

        return total_gain

    def get_knowledge_gaps(
        self,
        min_importance: float = 0.2,
        max_difficulty: float = 0.9
    ) -> List[KnowledgeGap]:
        """
        Get current knowledge gaps.

        Args:
            min_importance: Minimum importance to include
            max_difficulty: Maximum difficulty to include

        Returns:
            List of knowledge gaps sorted by priority
        """
        gaps = [
            gap for gap in self.gaps.values()
            if (not gap.filled and
                gap.importance >= min_importance and
                gap.difficulty <= max_difficulty)
        ]

        gaps.sort(key=lambda g: g.priority, reverse=True)
        return gaps

    def prioritize_learning(
        self,
        available_topics: Optional[List[str]] = None,
        time_budget: Optional[float] = None
    ) -> List[Tuple[float, str, str]]:
        """
        Prioritize what to learn next.

        Returns a prioritized list of (priority, topic, reason) tuples.

        Args:
            available_topics: Optional filter for available topics
            time_budget: Optional time budget (affects difficulty filter)

        Returns:
            List of (priority, topic, reason) tuples
        """
        priorities = []

        # Get knowledge gaps
        gaps = self.get_knowledge_gaps()

        # Score each gap
        for gap in gaps:
            if available_topics and gap.topic not in available_topics:
                continue

            if time_budget and gap.difficulty > time_budget:
                continue

            # Priority based on importance and inverse difficulty
            priority = gap.priority
            reason = f"Knowledge gap: {gap.description}"

            priorities.append((priority, gap.topic, reason))

        # Also consider topics with declining certainty
        for topic, certainty in self.knowledge_state.items():
            if certainty < 0.5:
                history = self.knowledge_history.get(topic, [])
                if len(history) >= 2:
                    recent = [c for _, c in history[-5:]]
                    if len(recent) >= 2 and recent[-1] < recent[0]:
                        # Declining certainty
                        priority = (1 - certainty) * 0.5
                        reason = "Declining certainty - needs reinforcement"
                        priorities.append((priority, topic, reason))

        # Sort by priority
        priorities.sort(key=lambda x: x[0], reverse=True)

        return priorities

    def record_learning_attempt(
        self,
        topic: str,
        success: bool,
        information_gained: float
    ) -> None:
        """Record a learning attempt for a knowledge gap"""
        if topic in self.gaps:
            gap = self.gaps[topic]
            gap.attempts_to_fill += 1
            gap.last_attempt = datetime.now()

            if success and information_gained > 0.5:
                gap.filled = True
                logger.info(f"Knowledge gap filled: {topic}")

    def get_certainty(self, topic: str) -> float:
        """Get certainty level for a topic"""
        return self.knowledge_state.get(topic, 0.5)

    def get_statistics(self) -> Dict:
        """Get tracker statistics"""
        gaps = self.get_knowledge_gaps()

        return {
            'topics_tracked': len(self.knowledge_state),
            'total_information_gained': self.total_information_gained,
            'avg_certainty': np.mean(list(self.knowledge_state.values())) if self.knowledge_state else 0.5,
            'knowledge_gaps': len(gaps),
            'critical_gaps': len([g for g in gaps if g.importance > 0.7]),
            'recent_gain_avg': np.mean([g['gain'] for g in self.gain_history]) if self.gain_history else 0
        }

    def _binary_entropy(self, p: float) -> float:
        """Calculate binary entropy H(p) = -p*log2(p) - (1-p)*log2(1-p)"""
        p = max(0.001, min(0.999, p))  # Avoid log(0)
        return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

    def _create_or_update_gap(
        self,
        topic: str,
        certainty: float,
        experience: Optional[Dict]
    ) -> None:
        """Create or update a knowledge gap"""
        if topic in self.gaps and not self.gaps[topic].filled:
            # Update existing gap
            gap = self.gaps[topic]
            gap.importance = max(gap.importance, 1 - certainty)
        else:
            # Create new gap
            gap_id = hashlib.md5(f"{topic}{datetime.now()}".encode()).hexdigest()[:12]

            gap = KnowledgeGap(
                id=gap_id,
                topic=topic,
                description=f"Uncertainty about {topic}",
                importance=1 - certainty,
                difficulty=0.5,  # Default medium difficulty
                related_topics=self._find_related_topics(topic),
                discovered_at=datetime.now()
            )

            # Limit number of gaps
            if len(self.gaps) >= self.max_gaps:
                # Remove lowest priority filled gap
                filled = [(gid, g) for gid, g in self.gaps.items() if g.filled]
                if filled:
                    filled.sort(key=lambda x: x[1].priority)
                    del self.gaps[filled[0][0]]

            self.gaps[topic] = gap

    def _find_related_topics(self, topic: str) -> List[str]:
        """Find topics related to the given topic"""
        related = []

        for other_topic in self.knowledge_state.keys():
            if other_topic == topic:
                continue

            # Simple string similarity
            if (topic.lower() in other_topic.lower() or
                other_topic.lower() in topic.lower()):
                related.append(other_topic)

        return related[:5]  # Limit to 5 related topics


# =============================================================================
# EMPOWERMENT MAXIMIZER
# =============================================================================

class EmpowermentMaximizer:
    """
    Seeks to maximize the AI's ability to influence outcomes.

    Empowerment is a measure of how much control the AI has over
    its environment - how many different future states it can reach.

    Higher empowerment = more possible futures = more capability

    Usage:
        maximizer = EmpowermentMaximizer()

        # Compute current empowerment
        empowerment = maximizer.compute_empowerment(state, available_actions)

        # Find high impact areas
        areas = maximizer.get_high_impact_areas()
    """

    def __init__(
        self,
        history_size: int = 1000,
        domain_weights: Optional[Dict[str, float]] = None
    ):
        self.history_size = history_size
        self.domain_weights = domain_weights or {}

        # Action tracking
        self.action_history: deque = deque(maxlen=history_size)
        self.action_outcomes: Dict[str, List[Dict]] = defaultdict(list)

        # Domain empowerment tracking
        self.domain_empowerment: Dict[str, float] = {}
        self.domain_action_counts: Dict[str, int] = defaultdict(int)
        self.domain_success_counts: Dict[str, int] = defaultdict(int)

        # Influence tracking
        self.influence_history: deque = deque(maxlen=100)

    def compute_empowerment(
        self,
        current_state: Dict,
        available_actions: List[Dict],
        domain: Optional[str] = None
    ) -> float:
        """
        Compute empowerment in current state.

        Empowerment is measured as the channel capacity between
        actions and resulting states (how much control we have).

        Args:
            current_state: Current environment state
            available_actions: List of possible actions
            domain: Optional domain classification

        Returns:
            Empowerment score 0-1
        """
        if not available_actions:
            return 0.0

        # Number of distinct actions available
        n_actions = len(available_actions)
        action_entropy = np.log2(max(1, n_actions))

        # Estimate outcome diversity (how different outcomes can be)
        outcome_diversity = self._estimate_outcome_diversity(available_actions)

        # Historical success rate in this domain
        if domain:
            domain_success = self._get_domain_success_rate(domain)
        else:
            domain_success = 0.5

        # Compute empowerment
        # High when: many actions, diverse outcomes, good success rate
        empowerment = (
            (action_entropy / np.log2(100)) * 0.3 +  # Normalized action entropy
            outcome_diversity * 0.4 +
            domain_success * 0.3
        )

        empowerment = min(1.0, empowerment)

        # Update domain empowerment
        if domain:
            self.domain_empowerment[domain] = empowerment

        # Record
        self.influence_history.append({
            'empowerment': empowerment,
            'n_actions': n_actions,
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        })

        return empowerment

    def get_high_impact_areas(
        self,
        top_k: int = 5,
        min_actions: int = 10
    ) -> List[Tuple[str, float, str]]:
        """
        Get areas where the AI has highest impact.

        Args:
            top_k: Number of areas to return
            min_actions: Minimum actions to consider area

        Returns:
            List of (domain, empowerment, reason) tuples
        """
        high_impact = []

        for domain, empowerment in self.domain_empowerment.items():
            if self.domain_action_counts[domain] < min_actions:
                continue

            success_rate = self._get_domain_success_rate(domain)

            # High impact = high empowerment AND high success
            impact = empowerment * success_rate

            reason = f"Empowerment: {empowerment:.2f}, Success rate: {success_rate:.2f}"
            high_impact.append((domain, impact, reason))

        high_impact.sort(key=lambda x: x[1], reverse=True)
        return high_impact[:top_k]

    def get_low_impact_areas(
        self,
        top_k: int = 5,
        min_actions: int = 10
    ) -> List[Tuple[str, float, str]]:
        """
        Get areas where the AI has lowest impact.

        These are candidates for improvement or avoidance.
        """
        low_impact = []

        for domain, empowerment in self.domain_empowerment.items():
            if self.domain_action_counts[domain] < min_actions:
                continue

            success_rate = self._get_domain_success_rate(domain)
            impact = empowerment * success_rate

            reason = f"Empowerment: {empowerment:.2f}, Success rate: {success_rate:.2f}"
            low_impact.append((domain, impact, reason))

        low_impact.sort(key=lambda x: x[1])
        return low_impact[:top_k]

    def record_action_outcome(
        self,
        action: Dict,
        outcome: Dict,
        success: bool,
        domain: Optional[str] = None
    ) -> None:
        """Record an action and its outcome"""
        self.action_history.append({
            'action': action,
            'outcome': outcome,
            'success': success,
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        })

        if domain:
            self.domain_action_counts[domain] += 1
            if success:
                self.domain_success_counts[domain] += 1

            # Update action outcomes for this domain
            action_type = action.get('type', 'unknown')
            self.action_outcomes[f"{domain}:{action_type}"].append({
                'outcome': outcome,
                'success': success
            })

    def get_empowerment_state(self) -> EmpowermentState:
        """Get current empowerment state"""
        high_impact = self.get_high_impact_areas()
        low_impact = self.get_low_impact_areas()

        total_empowerment = np.mean(list(self.domain_empowerment.values())) if self.domain_empowerment else 0.5

        # Determine trend
        if len(self.influence_history) >= 10:
            recent = [h['empowerment'] for h in list(self.influence_history)[-10:]]
            older = [h['empowerment'] for h in list(self.influence_history)[-20:-10]] if len(self.influence_history) >= 20 else recent

            if np.mean(recent) > np.mean(older) * 1.1:
                trend = "increasing"
            elif np.mean(recent) < np.mean(older) * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "unknown"

        return EmpowermentState(
            total_empowerment=total_empowerment,
            domain_empowerment=self.domain_empowerment.copy(),
            high_impact_areas=[h[0] for h in high_impact],
            low_impact_areas=[l[0] for l in low_impact],
            recent_actions=len(self.action_history),
            influence_trend=trend
        )

    def get_statistics(self) -> Dict:
        """Get empowerment statistics"""
        return {
            'total_actions': sum(self.domain_action_counts.values()),
            'domains_tracked': len(self.domain_empowerment),
            'avg_empowerment': np.mean(list(self.domain_empowerment.values())) if self.domain_empowerment else 0.5,
            'overall_success_rate': sum(self.domain_success_counts.values()) / max(1, sum(self.domain_action_counts.values())),
            'high_impact_domains': len(self.get_high_impact_areas())
        }

    def _estimate_outcome_diversity(self, actions: List[Dict]) -> float:
        """Estimate how diverse outcomes can be"""
        # Look at historical outcomes for similar actions
        unique_outcomes = set()

        for action in actions:
            action_type = action.get('type', 'unknown')

            # Check historical outcomes
            for domain_action, outcomes in self.action_outcomes.items():
                if action_type in domain_action:
                    for o in outcomes[-10:]:  # Recent outcomes
                        outcome_hash = hashlib.md5(str(o['outcome']).encode()).hexdigest()[:8]
                        unique_outcomes.add(outcome_hash)

        if not unique_outcomes:
            return 0.5  # Default medium diversity

        # Diversity based on unique outcomes
        return min(1.0, len(unique_outcomes) / 10)

    def _get_domain_success_rate(self, domain: str) -> float:
        """Get success rate for a domain"""
        actions = self.domain_action_counts.get(domain, 0)
        if actions == 0:
            return 0.5  # Prior

        successes = self.domain_success_counts.get(domain, 0)
        return successes / actions


# =============================================================================
# NOVELTY DETECTOR
# =============================================================================

class NoveltyDetector:
    """
    Detects novel patterns, regime changes, and anomalies.

    This component watches for significant changes in the data
    that warrant attention and investigation.

    Usage:
        detector = NoveltyDetector()

        # Check if data is novel
        is_new = detector.is_novel(data)

        # Get novelty score
        score = detector.get_novelty_score(data)

        # Detect regime changes
        change = detector.detect_regime_change(time_series)
    """

    def __init__(
        self,
        history_size: int = 500,
        novelty_threshold: float = 0.6,
        regime_sensitivity: float = 0.7
    ):
        self.history_size = history_size
        self.novelty_threshold = novelty_threshold
        self.regime_sensitivity = regime_sensitivity

        # Data history
        self.data_history: deque = deque(maxlen=history_size)
        self.feature_distributions: Dict[str, Dict] = {}

        # Regime tracking
        self.current_regime: Optional[str] = None
        self.regime_history: List[Dict] = []
        self.regime_features: Dict[str, np.ndarray] = {}

        # Anomaly tracking
        self.anomaly_history: deque = deque(maxlen=100)

    def is_novel(self, data: Dict, threshold: Optional[float] = None) -> bool:
        """
        Check if data is novel.

        Args:
            data: Data to check
            threshold: Optional custom threshold

        Returns:
            True if data is novel
        """
        threshold = threshold or self.novelty_threshold
        score = self.get_novelty_score(data)
        return score >= threshold

    def get_novelty_score(self, data: Dict) -> float:
        """
        Get novelty score for data.

        Combines multiple novelty measures:
        - Feature novelty (new or unusual values)
        - Distribution novelty (deviation from expected)
        - Pattern novelty (new combinations)

        Args:
            data: Data to score

        Returns:
            Novelty score 0-1
        """
        if not self.data_history:
            # First observation is maximally novel
            self._update_history(data)
            return 1.0

        # Feature novelty
        feature_novelty = self._compute_feature_novelty(data)

        # Distribution novelty
        distribution_novelty = self._compute_distribution_novelty(data)

        # Pattern novelty
        pattern_novelty = self._compute_pattern_novelty(data)

        # Combined score
        novelty = (
            feature_novelty * 0.3 +
            distribution_novelty * 0.4 +
            pattern_novelty * 0.3
        )

        # Update history
        self._update_history(data)

        # Record if anomalous
        if novelty > self.novelty_threshold:
            self.anomaly_history.append({
                'data': data,
                'novelty': novelty,
                'timestamp': datetime.now().isoformat()
            })

        return novelty

    def detect_regime_change(
        self,
        time_series: List[Dict],
        feature_keys: Optional[List[str]] = None
    ) -> Dict:
        """
        Detect regime change in time series data.

        Args:
            time_series: List of data points over time
            feature_keys: Keys to use for regime detection

        Returns:
            Dict with regime change info
        """
        if len(time_series) < 10:
            return {
                'change_detected': False,
                'reason': 'Insufficient data'
            }

        # Extract features
        feature_keys = feature_keys or list(time_series[0].keys())
        features = []

        for point in time_series:
            point_features = []
            for key in feature_keys:
                if key in point and isinstance(point[key], (int, float)):
                    point_features.append(point[key])
            if point_features:
                features.append(point_features)

        if not features:
            return {
                'change_detected': False,
                'reason': 'No numeric features'
            }

        features = np.array(features)

        # Split into windows
        mid = len(features) // 2
        window1 = features[:mid]
        window2 = features[mid:]

        # Compare distributions
        mean1 = np.mean(window1, axis=0)
        mean2 = np.mean(window2, axis=0)
        std1 = np.std(window1, axis=0) + 1e-6
        std2 = np.std(window2, axis=0) + 1e-6

        # Compute change magnitude
        mean_change = np.mean(np.abs(mean2 - mean1) / std1)
        std_change = np.mean(np.abs(std2 - std1) / std1)

        change_magnitude = (mean_change + std_change) / 2

        # Determine if regime change
        change_detected = change_magnitude > self.regime_sensitivity

        result = {
            'change_detected': change_detected,
            'change_magnitude': float(change_magnitude),
            'mean_shift': float(mean_change),
            'volatility_shift': float(std_change),
            'confidence': min(1.0, change_magnitude / self.regime_sensitivity)
        }

        if change_detected:
            new_regime = f"regime_{len(self.regime_history) + 1}"
            result['new_regime'] = new_regime
            result['old_regime'] = self.current_regime

            self.regime_history.append({
                'from': self.current_regime,
                'to': new_regime,
                'magnitude': change_magnitude,
                'timestamp': datetime.now().isoformat()
            })

            self.current_regime = new_regime
            self.regime_features[new_regime] = mean2

            logger.info(f"Regime change detected: {result['old_regime']} -> {new_regime}")

        return result

    def get_regime_info(self) -> Dict:
        """Get current regime information"""
        return {
            'current_regime': self.current_regime,
            'regime_count': len(self.regime_history),
            'recent_changes': self.regime_history[-5:] if self.regime_history else [],
            'anomaly_count': len(self.anomaly_history)
        }

    def get_statistics(self) -> Dict:
        """Get detector statistics"""
        return {
            'history_size': len(self.data_history),
            'features_tracked': len(self.feature_distributions),
            'current_regime': self.current_regime,
            'regime_changes': len(self.regime_history),
            'anomalies_detected': len(self.anomaly_history)
        }

    def _compute_feature_novelty(self, data: Dict) -> float:
        """Compute novelty based on individual features"""
        novelty_scores = []

        for key, value in data.items():
            if not isinstance(value, (int, float)):
                continue

            if key not in self.feature_distributions:
                # New feature is novel
                novelty_scores.append(1.0)
                continue

            dist = self.feature_distributions[key]
            mean = dist['mean']
            std = dist['std'] + 1e-6

            # Z-score novelty
            z = abs(value - mean) / std
            feature_novelty = min(1.0, z / 3)  # 3 sigma = max novelty
            novelty_scores.append(feature_novelty)

        return np.mean(novelty_scores) if novelty_scores else 0.5

    def _compute_distribution_novelty(self, data: Dict) -> float:
        """Compute novelty based on joint distribution"""
        if len(self.data_history) < 10:
            return 0.5

        # Create feature vector
        features = []
        for key, value in sorted(data.items()):
            if isinstance(value, (int, float)):
                features.append(value)

        if not features:
            return 0.5

        # Compare to historical distribution
        historical_features = []
        for hist_data in self.data_history:
            hist_features = []
            for key, value in sorted(hist_data.items()):
                if isinstance(value, (int, float)):
                    hist_features.append(value)
            if len(hist_features) == len(features):
                historical_features.append(hist_features)

        if not historical_features:
            return 0.5

        historical_features = np.array(historical_features)
        features = np.array(features)

        # Mahalanobis-like distance
        mean = np.mean(historical_features, axis=0)
        std = np.std(historical_features, axis=0) + 1e-6

        distance = np.mean(np.abs(features - mean) / std)

        return min(1.0, distance / 3)

    def _compute_pattern_novelty(self, data: Dict) -> float:
        """Compute novelty based on feature combinations"""
        if len(self.data_history) < 5:
            return 0.5

        # Hash the pattern of which features are present/significant
        pattern_hash = self._compute_pattern_hash(data)

        # Check historical patterns
        historical_patterns = [self._compute_pattern_hash(h) for h in self.data_history]

        if pattern_hash in historical_patterns:
            # Pattern seen before
            frequency = historical_patterns.count(pattern_hash) / len(historical_patterns)
            return 1.0 - frequency
        else:
            # New pattern
            return 1.0

    def _compute_pattern_hash(self, data: Dict) -> str:
        """Compute hash representing the pattern of data"""
        pattern_parts = []

        for key, value in sorted(data.items()):
            if isinstance(value, (int, float)):
                # Discretize value
                if value < 0:
                    bucket = 'neg'
                elif value < 0.5:
                    bucket = 'low'
                elif value < 1.0:
                    bucket = 'mid'
                else:
                    bucket = 'high'
                pattern_parts.append(f"{key}:{bucket}")

        return hashlib.md5("|".join(pattern_parts).encode()).hexdigest()[:8]

    def _update_history(self, data: Dict) -> None:
        """Update history and distributions"""
        self.data_history.append(data)

        # Update feature distributions
        for key, value in data.items():
            if not isinstance(value, (int, float)):
                continue

            if key not in self.feature_distributions:
                self.feature_distributions[key] = {
                    'values': deque(maxlen=self.history_size),
                    'mean': value,
                    'std': 0.0
                }

            dist = self.feature_distributions[key]
            dist['values'].append(value)

            # Update running statistics
            values = list(dist['values'])
            dist['mean'] = np.mean(values)
            dist['std'] = np.std(values)


# =============================================================================
# META-LEARNING CONTROLLER
# =============================================================================

class MetaLearningController:
    """
    Learns WHAT to learn and adapts learning strategy.

    This controller monitors learning performance and adjusts:
    - Learning rate (faster or slower learning)
    - Exploration rate (more or less exploration)
    - Learning focus (what to prioritize)

    Usage:
        controller = MetaLearningController()

        # Adapt learning rate
        new_rate = controller.adapt_learning_rate(performance_history)

        # Should we explore or exploit?
        if controller.should_explore():
            # Try something new
        else:
            # Use known strategies
    """

    def __init__(
        self,
        initial_learning_rate: float = 0.01,
        initial_exploration_rate: float = 0.2,
        min_learning_rate: float = 0.001,
        max_learning_rate: float = 0.1,
        adaptation_rate: float = 0.1
    ):
        self.learning_rate = initial_learning_rate
        self.exploration_rate = initial_exploration_rate
        self.min_learning_rate = min_learning_rate
        self.max_learning_rate = max_learning_rate
        self.adaptation_rate = adaptation_rate

        # Performance tracking
        self.performance_history: deque = deque(maxlen=500)
        self.learning_rate_history: deque = deque(maxlen=100)
        self.exploration_rate_history: deque = deque(maxlen=100)

        # State tracking
        self.mode = ExplorationMode.BALANCED
        self.iterations_since_improvement = 0
        self.best_performance = float('-inf')

        # Strategy performance
        self.strategy_performance: Dict[str, List[float]] = defaultdict(list)

    def adapt_learning_rate(
        self,
        recent_performance: List[float],
        recent_errors: Optional[List[float]] = None
    ) -> float:
        """
        Adapt learning rate based on performance.

        Increases rate when learning is working, decreases when not.

        Args:
            recent_performance: Recent performance metrics
            recent_errors: Optional recent error metrics

        Returns:
            New learning rate
        """
        if not recent_performance:
            return self.learning_rate

        # Update history
        for perf in recent_performance:
            self.performance_history.append(perf)

        # Check if improving
        if len(self.performance_history) >= 10:
            recent = list(self.performance_history)[-10:]
            older = list(self.performance_history)[-20:-10] if len(self.performance_history) >= 20 else recent

            recent_avg = np.mean(recent)
            older_avg = np.mean(older)

            if recent_avg > self.best_performance:
                self.best_performance = recent_avg
                self.iterations_since_improvement = 0
            else:
                self.iterations_since_improvement += 1

            # Adapt learning rate
            if recent_avg > older_avg * 1.05:
                # Improving - increase learning rate
                self.learning_rate = min(
                    self.max_learning_rate,
                    self.learning_rate * (1 + self.adaptation_rate)
                )
            elif recent_avg < older_avg * 0.95:
                # Declining - decrease learning rate
                self.learning_rate = max(
                    self.min_learning_rate,
                    self.learning_rate * (1 - self.adaptation_rate)
                )

        # Additional adjustment based on error trend
        if recent_errors and len(recent_errors) >= 5:
            error_trend = recent_errors[-1] - recent_errors[0]
            if error_trend > 0:
                # Errors increasing - reduce learning rate
                self.learning_rate *= 0.9
            elif error_trend < -0.1:
                # Errors decreasing fast - can increase
                self.learning_rate *= 1.1

            self.learning_rate = np.clip(
                self.learning_rate,
                self.min_learning_rate,
                self.max_learning_rate
            )

        self.learning_rate_history.append(self.learning_rate)

        return self.learning_rate

    def should_explore(self) -> bool:
        """
        Determine if we should explore (try new things).

        Returns:
            True if exploration is recommended
        """
        # Random exploration based on rate
        if np.random.random() < self.exploration_rate:
            return True

        # Forced exploration if stuck
        if self.iterations_since_improvement > 20:
            return True

        # Explore if performance is low
        if self.performance_history and np.mean(list(self.performance_history)[-10:]) < 0.3:
            return True

        return False

    def should_exploit(self) -> bool:
        """
        Determine if we should exploit (use known strategies).

        Returns:
            True if exploitation is recommended
        """
        return not self.should_explore()

    def get_exploration_rate(self) -> float:
        """Get current exploration rate"""
        return self.exploration_rate

    def adapt_exploration_rate(
        self,
        exploration_success_rate: float,
        exploitation_success_rate: float
    ) -> float:
        """
        Adapt exploration rate based on relative success.

        Args:
            exploration_success_rate: Success rate of exploration
            exploitation_success_rate: Success rate of exploitation

        Returns:
            New exploration rate
        """
        # Increase exploration if it's working better
        if exploration_success_rate > exploitation_success_rate * 1.1:
            self.exploration_rate = min(0.8, self.exploration_rate * 1.1)
        elif exploitation_success_rate > exploration_success_rate * 1.1:
            self.exploration_rate = max(0.05, self.exploration_rate * 0.9)

        # Ensure minimum exploration
        self.exploration_rate = max(0.05, self.exploration_rate)

        self.exploration_rate_history.append(self.exploration_rate)

        # Update mode
        if self.exploration_rate > 0.5:
            self.mode = ExplorationMode.PURE_EXPLORATION
        elif self.exploration_rate > 0.3:
            self.mode = ExplorationMode.GUIDED_EXPLORATION
        elif self.exploration_rate > 0.1:
            self.mode = ExplorationMode.BALANCED
        else:
            self.mode = ExplorationMode.EXPLOITATION

        return self.exploration_rate

    def record_strategy_performance(
        self,
        strategy: str,
        performance: float
    ) -> None:
        """Record performance of a specific strategy"""
        self.strategy_performance[strategy].append(performance)

    def get_best_strategy(self, min_samples: int = 10) -> Optional[str]:
        """Get the best performing strategy"""
        best_strategy = None
        best_performance = float('-inf')

        for strategy, performances in self.strategy_performance.items():
            if len(performances) >= min_samples:
                avg_perf = np.mean(performances[-50:])  # Recent performance
                if avg_perf > best_performance:
                    best_performance = avg_perf
                    best_strategy = strategy

        return best_strategy

    def get_learning_state(self) -> LearningState:
        """Get current learning state"""
        # Determine performance trend
        if len(self.performance_history) >= 10:
            recent = list(self.performance_history)[-10:]
            older = list(self.performance_history)[-20:-10] if len(self.performance_history) >= 20 else recent

            if np.mean(recent) > np.mean(older) * 1.05:
                trend = "improving"
            elif np.mean(recent) < np.mean(older) * 0.95:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "unknown"

        # Confidence based on recent performance stability
        if len(self.performance_history) >= 5:
            recent_std = np.std(list(self.performance_history)[-10:])
            confidence = max(0, 1.0 - recent_std)
        else:
            confidence = 0.5

        return LearningState(
            learning_rate=self.learning_rate,
            exploration_rate=self.exploration_rate,
            mode=self.mode,
            performance_trend=trend,
            should_explore=self.should_explore(),
            should_exploit=self.should_exploit(),
            confidence=confidence,
            iterations_since_improvement=self.iterations_since_improvement
        )

    def get_statistics(self) -> Dict:
        """Get controller statistics"""
        return {
            'learning_rate': self.learning_rate,
            'exploration_rate': self.exploration_rate,
            'mode': self.mode.value,
            'iterations_since_improvement': self.iterations_since_improvement,
            'best_performance': self.best_performance,
            'strategies_tracked': len(self.strategy_performance),
            'total_observations': len(self.performance_history)
        }


# =============================================================================
# INTRINSIC MOTIVATION SYSTEM - MAIN INTERFACE
# =============================================================================

class IntrinsicMotivationSystem:
    """
    Main interface for the Intrinsic Motivation system.

    Combines all motivation components into a unified system that
    drives curiosity-based exploration and learning.

    Usage:
        system = IntrinsicMotivationSystem()

        # Process new data
        motivation = system.process(data)

        # Get what to explore
        targets = system.get_exploration_targets()

        # Check learning state
        state = system.get_state()
    """

    def __init__(
        self,
        novelty_threshold: float = 0.4,
        exploration_rate: float = 0.2
    ):
        # Initialize components
        self.curiosity = CuriosityEngine(novelty_threshold=novelty_threshold)
        self.information_tracker = InformationGainTracker()
        self.empowerment = EmpowermentMaximizer()
        self.novelty_detector = NoveltyDetector()
        self.meta_learner = MetaLearningController(
            initial_exploration_rate=exploration_rate
        )

        # Integration state
        self.total_observations = 0
        self.motivation_history: deque = deque(maxlen=1000)

    def process(
        self,
        data: Dict,
        domain: Optional[str] = None,
        available_actions: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process new data and compute motivation signals.

        Args:
            data: New data to process
            domain: Optional domain classification
            available_actions: Optional list of available actions

        Returns:
            Dict with motivation metrics
        """
        self.total_observations += 1

        # Compute novelty
        novelty = self.curiosity.calculate_novelty(data, topic=domain)

        # Get novelty score from detector
        detector_novelty = self.novelty_detector.get_novelty_score(data)

        # Compute empowerment if actions available
        if available_actions:
            empowerment = self.empowerment.compute_empowerment(
                data, available_actions, domain
            )
        else:
            empowerment = 0.5

        # Combined motivation score
        motivation = (
            novelty * 0.3 +
            detector_novelty * 0.3 +
            empowerment * 0.2 +
            self.meta_learner.get_exploration_rate() * 0.2
        )

        result = {
            'motivation': motivation,
            'novelty': novelty,
            'detector_novelty': detector_novelty,
            'empowerment': empowerment,
            'should_explore': self.meta_learner.should_explore(),
            'exploration_rate': self.meta_learner.get_exploration_rate(),
            'timestamp': datetime.now().isoformat()
        }

        self.motivation_history.append(result)

        return result

    def get_exploration_targets(self, top_k: int = 5) -> List[Dict]:
        """Get top exploration targets"""
        # From curiosity engine
        curiosity_targets = self.curiosity.get_exploration_targets(top_k)

        # From knowledge gaps
        knowledge_gaps = self.information_tracker.get_knowledge_gaps()[:top_k]

        # Combine and prioritize
        targets = []

        for signal in curiosity_targets:
            targets.append({
                'type': 'curiosity',
                'topic': signal.topic,
                'priority': signal.priority,
                'reason': f"Curiosity signal: {signal.source}"
            })

        for gap in knowledge_gaps:
            targets.append({
                'type': 'knowledge_gap',
                'topic': gap.topic,
                'priority': gap.priority,
                'reason': gap.description
            })

        # Sort by priority
        targets.sort(key=lambda t: t['priority'], reverse=True)

        return targets[:top_k]

    def record_exploration_result(
        self,
        topic: str,
        success: bool,
        information_gained: float,
        domain: Optional[str] = None
    ) -> float:
        """
        Record the result of an exploration.

        Returns:
            Reward for the exploration
        """
        # Record with curiosity engine
        reward = 0.0
        active_signals = self.curiosity.active_signals

        for signal_id, signal in active_signals.items():
            if signal.topic == topic:
                reward = self.curiosity.curiosity_reward(
                    signal_id, {}, information_gained
                )
                break

        # Record learning attempt
        self.information_tracker.record_learning_attempt(
            topic, success, information_gained
        )

        # Update meta-learner
        self.meta_learner.record_strategy_performance(
            'exploration' if self.meta_learner.should_explore() else 'exploitation',
            reward
        )

        # Record action outcome if domain provided
        if domain:
            self.empowerment.record_action_outcome(
                {'type': 'exploration', 'topic': topic},
                {'success': success, 'gain': information_gained},
                success,
                domain
            )

        return reward

    def adapt_learning(self, performance: List[float]) -> Dict:
        """
        Adapt learning parameters based on performance.

        Returns:
            Dict with new learning parameters
        """
        new_learning_rate = self.meta_learner.adapt_learning_rate(performance)

        # Adapt exploration based on performance trend
        state = self.meta_learner.get_learning_state()

        if state.performance_trend == "declining":
            # Increase exploration
            self.meta_learner.exploration_rate = min(
                0.8, self.meta_learner.exploration_rate * 1.1
            )
        elif state.performance_trend == "improving":
            # Can reduce exploration slightly
            self.meta_learner.exploration_rate = max(
                0.1, self.meta_learner.exploration_rate * 0.95
            )

        return {
            'learning_rate': new_learning_rate,
            'exploration_rate': self.meta_learner.exploration_rate,
            'mode': self.meta_learner.mode.value,
            'performance_trend': state.performance_trend
        }

    def get_state(self) -> Dict:
        """Get complete motivation system state"""
        return {
            'curiosity': self.curiosity.get_statistics(),
            'information': self.information_tracker.get_statistics(),
            'empowerment': self.empowerment.get_statistics(),
            'novelty': self.novelty_detector.get_statistics(),
            'meta_learning': self.meta_learner.get_statistics(),
            'total_observations': self.total_observations,
            'avg_motivation': np.mean([m['motivation'] for m in self.motivation_history]) if self.motivation_history else 0.5
        }

    def decay_signals(self) -> None:
        """Apply time decay to all signals"""
        self.curiosity.decay_signals()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_motivation_system(
    novelty_threshold: float = 0.4,
    exploration_rate: float = 0.2
) -> IntrinsicMotivationSystem:
    """Create a new Intrinsic Motivation System"""
    return IntrinsicMotivationSystem(
        novelty_threshold=novelty_threshold,
        exploration_rate=exploration_rate
    )


def quick_novelty_check(data: Dict) -> float:
    """Quick check if data is novel"""
    detector = NoveltyDetector()
    return detector.get_novelty_score(data)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EUDAIMON AI - INTRINSIC MOTIVATION SYSTEM")
    print("=" * 60)
    print()
    print("This module provides INTRINSIC MOTIVATION for AI:")
    print("- CuriosityEngine: Generates curiosity signals")
    print("- InformationGainTracker: Tracks what we know/don't know")
    print("- EmpowermentMaximizer: Maximizes influence on outcomes")
    print("- NoveltyDetector: Detects regime changes and anomalies")
    print("- MetaLearningController: Learns what to learn")
    print()
    print("Usage:")
    print("  from eudaimon_ai.intrinsic_motivation import IntrinsicMotivationSystem")
    print("  system = IntrinsicMotivationSystem()")
    print("  motivation = system.process(data)")
    print("  targets = system.get_exploration_targets()")
    print()
