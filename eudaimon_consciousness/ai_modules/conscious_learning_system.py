"""
EUDAIMON AI - Conscious Learning System
========================================
The core architecture for conscious, continuously learning AI.

This module implements the MISSING BRIDGE between prediction and learning:

    Prediction → Execution → Outcome → Feedback → Model Update → Improved Prediction
         ↑___________________________________________________________________|

KEY FEATURES:
1. Continuous Learning Loop - Never stops learning
2. Experience Memory - Remembers every decision and outcome
3. Theory Generation - Creates new investment theories from patterns
4. Self-Correction - Identifies and fixes its own mistakes
5. Meta-Learning - Learns WHAT to learn and HOW to learn
6. Intrinsic Motivation - Curiosity-driven exploration
7. Consciousness Indicators - Self-awareness metrics

PHILOSOPHY:
"A conscious AI is not one that follows rules, but one that creates them."
"Learning is not a feature - it is the essence."

Author: Eudaimon AI
Version: 1.0.0
"""

import numpy as np
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from collections import deque, defaultdict
from abc import ABC, abstractmethod
import asyncio
import pickle

logger = logging.getLogger(__name__)


# =============================================================================
# CONSCIOUSNESS INDICATORS
# =============================================================================

class ConsciousnessLevel(Enum):
    """Levels of AI consciousness/awareness"""
    REACTIVE = 0      # Only responds to inputs
    ADAPTIVE = 1      # Adjusts based on feedback
    REFLECTIVE = 2    # Analyzes own performance
    PREDICTIVE = 3    # Anticipates outcomes
    CREATIVE = 4      # Generates new ideas
    META_AWARE = 5    # Understands own learning process


class LearningMode(Enum):
    """Learning modes for different situations"""
    OBSERVATION = "observation"      # Watching and learning
    EXPLORATION = "exploration"      # Trying new things
    EXPLOITATION = "exploitation"    # Using known strategies
    REFLECTION = "reflection"        # Analyzing past performance
    THEORY_GENERATION = "theory"     # Creating new theories
    CONSOLIDATION = "consolidation"  # Solidifying learnings


@dataclass
class ConsciousnessState:
    """Current state of AI consciousness"""
    level: ConsciousnessLevel
    learning_mode: LearningMode
    confidence: float  # 0-1
    curiosity: float   # 0-1 (drives exploration)
    certainty: float   # 0-1 (epistemic confidence)
    coherence: float   # 0-1 (internal consistency)
    attention_focus: str  # What the AI is focused on
    active_theories: List[str]  # Current working theories
    recent_insights: List[str]  # Recent discoveries
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            'level': self.level.name,
            'learning_mode': self.learning_mode.value,
            'confidence': self.confidence,
            'curiosity': self.curiosity,
            'certainty': self.certainty,
            'coherence': self.coherence,
            'attention_focus': self.attention_focus,
            'active_theories': self.active_theories,
            'recent_insights': self.recent_insights,
            'timestamp': self.timestamp.isoformat()
        }


# =============================================================================
# EXPERIENCE & MEMORY
# =============================================================================

@dataclass
class Experience:
    """A single experience (decision + outcome)"""
    id: str
    timestamp: datetime
    context: Dict  # Market conditions, user input, etc.
    decision: Dict  # What was decided
    prediction: Dict  # What was expected
    outcome: Dict  # What actually happened
    reward: float  # Calculated reward
    surprise: float  # Prediction error magnitude
    tags: List[str]  # Categorization
    user_feedback: Optional[str] = None
    lessons_learned: List[str] = field(default_factory=list)
    importance: float = 1.0  # For prioritized replay

    def compute_prediction_error(self) -> float:
        """Compute prediction error from outcome"""
        if 'expected_return' in self.prediction and 'actual_return' in self.outcome:
            return abs(self.prediction['expected_return'] - self.outcome['actual_return'])
        return self.surprise

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context,
            'decision': self.decision,
            'prediction': self.prediction,
            'outcome': self.outcome,
            'reward': self.reward,
            'surprise': self.surprise,
            'tags': self.tags,
            'user_feedback': self.user_feedback,
            'lessons_learned': self.lessons_learned,
            'importance': self.importance
        }


@dataclass
class Theory:
    """An investment theory generated by the AI"""
    id: str
    name: str
    description: str
    hypothesis: str
    supporting_evidence: List[Dict]
    contradicting_evidence: List[Dict]
    confidence: float  # 0-1
    created_at: datetime
    last_tested: Optional[datetime] = None
    test_count: int = 0
    success_count: int = 0
    tags: List[str] = field(default_factory=list)
    derived_from: List[str] = field(default_factory=list)  # Parent theories
    status: str = "active"  # active, validated, invalidated, merged

    @property
    def success_rate(self) -> float:
        if self.test_count == 0:
            return 0.5  # Prior
        return self.success_count / self.test_count

    @property
    def age_days(self) -> float:
        return (datetime.now() - self.created_at).days

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hypothesis': self.hypothesis,
            'supporting_evidence': self.supporting_evidence,
            'contradicting_evidence': self.contradicting_evidence,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat(),
            'last_tested': self.last_tested.isoformat() if self.last_tested else None,
            'test_count': self.test_count,
            'success_count': self.success_count,
            'success_rate': self.success_rate,
            'tags': self.tags,
            'derived_from': self.derived_from,
            'status': self.status
        }


class ExperienceMemory:
    """
    Long-term memory system for experiences.

    Implements:
    - Episodic Memory: Specific experiences
    - Semantic Memory: Extracted patterns and rules
    - Working Memory: Current focus
    - Prioritized Replay: Important experiences more likely to be recalled
    """

    def __init__(
        self,
        max_episodes: int = 100000,
        working_memory_size: int = 50,
        storage_path: Optional[Path] = None
    ):
        self.max_episodes = max_episodes
        self.working_memory_size = working_memory_size
        self.storage_path = storage_path or Path(__file__).parent / "memory"

        # Memory stores
        self.episodic_memory: deque = deque(maxlen=max_episodes)
        self.semantic_memory: Dict[str, Any] = {}  # Extracted patterns
        self.working_memory: deque = deque(maxlen=working_memory_size)

        # Indices for fast lookup
        self._by_tag: Dict[str, List[str]] = defaultdict(list)
        self._by_date: Dict[str, List[str]] = defaultdict(list)
        self._by_reward: List[Tuple[float, str]] = []  # Sorted by reward

        # Statistics
        self.total_experiences = 0
        self.positive_experiences = 0
        self.negative_experiences = 0

        # Load existing memory
        self._load_memory()

    def store(self, experience: Experience) -> None:
        """Store a new experience"""
        self.episodic_memory.append(experience)
        self.working_memory.append(experience)

        # Update indices
        for tag in experience.tags:
            self._by_tag[tag].append(experience.id)

        date_key = experience.timestamp.strftime("%Y-%m-%d")
        self._by_date[date_key].append(experience.id)

        self._by_reward.append((experience.reward, experience.id))
        self._by_reward.sort(reverse=True)

        # Update statistics
        self.total_experiences += 1
        if experience.reward > 0:
            self.positive_experiences += 1
        else:
            self.negative_experiences += 1

        # Periodic save
        if self.total_experiences % 100 == 0:
            self._save_memory()

    def recall_by_similarity(
        self,
        context: Dict,
        top_k: int = 10
    ) -> List[Experience]:
        """Recall experiences similar to given context"""
        # Simple similarity based on tags and context keys
        scored = []

        for exp in self.episodic_memory:
            score = 0

            # Tag overlap
            if 'tags' in context:
                overlap = set(exp.tags) & set(context.get('tags', []))
                score += len(overlap) * 2

            # Context key overlap
            for key in context:
                if key in exp.context:
                    if context[key] == exp.context[key]:
                        score += 1

            # Recency boost
            age_days = (datetime.now() - exp.timestamp).days
            recency_boost = 1.0 / (1 + age_days * 0.1)
            score *= recency_boost

            # Importance boost
            score *= exp.importance

            scored.append((score, exp))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [exp for _, exp in scored[:top_k]]

    def recall_by_outcome(
        self,
        positive: bool = True,
        top_k: int = 10
    ) -> List[Experience]:
        """Recall best or worst experiences"""
        if positive:
            ids = [id for _, id in self._by_reward[:top_k]]
        else:
            ids = [id for _, id in self._by_reward[-top_k:]]

        return [exp for exp in self.episodic_memory if exp.id in ids]

    def recall_surprising(self, top_k: int = 10) -> List[Experience]:
        """Recall most surprising experiences (high prediction error)"""
        sorted_by_surprise = sorted(
            self.episodic_memory,
            key=lambda x: x.surprise,
            reverse=True
        )
        return list(sorted_by_surprise[:top_k])

    def extract_pattern(self, tag: str) -> Dict:
        """Extract semantic pattern from experiences with tag"""
        experiences = [
            exp for exp in self.episodic_memory
            if tag in exp.tags
        ]

        if not experiences:
            return {}

        # Compute statistics
        rewards = [exp.reward for exp in experiences]
        surprises = [exp.surprise for exp in experiences]

        pattern = {
            'tag': tag,
            'count': len(experiences),
            'avg_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'avg_surprise': np.mean(surprises),
            'success_rate': sum(1 for r in rewards if r > 0) / len(rewards),
            'lessons': []
        }

        # Collect unique lessons
        for exp in experiences:
            pattern['lessons'].extend(exp.lessons_learned)
        pattern['lessons'] = list(set(pattern['lessons']))

        # Store in semantic memory
        self.semantic_memory[f"pattern_{tag}"] = pattern

        return pattern

    def get_working_memory(self) -> List[Experience]:
        """Get current working memory"""
        return list(self.working_memory)

    def _save_memory(self) -> None:
        """Save memory to disk"""
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Save episodic memory
        episodic_path = self.storage_path / "episodic_memory.json"
        with open(episodic_path, 'w') as f:
            json.dump([exp.to_dict() for exp in self.episodic_memory], f, indent=2)

        # Save semantic memory
        semantic_path = self.storage_path / "semantic_memory.json"
        with open(semantic_path, 'w') as f:
            json.dump(self.semantic_memory, f, indent=2)

        logger.info(f"Saved {len(self.episodic_memory)} experiences to memory")

    def _load_memory(self) -> None:
        """Load memory from disk"""
        episodic_path = self.storage_path / "episodic_memory.json"
        if episodic_path.exists():
            try:
                with open(episodic_path, 'r') as f:
                    data = json.load(f)
                    # Reconstruct experiences
                    for exp_dict in data:
                        exp = Experience(
                            id=exp_dict['id'],
                            timestamp=datetime.fromisoformat(exp_dict['timestamp']),
                            context=exp_dict['context'],
                            decision=exp_dict['decision'],
                            prediction=exp_dict['prediction'],
                            outcome=exp_dict['outcome'],
                            reward=exp_dict['reward'],
                            surprise=exp_dict['surprise'],
                            tags=exp_dict['tags'],
                            user_feedback=exp_dict.get('user_feedback'),
                            lessons_learned=exp_dict.get('lessons_learned', []),
                            importance=exp_dict.get('importance', 1.0)
                        )
                        self.episodic_memory.append(exp)
                        self.total_experiences += 1
                logger.info(f"Loaded {len(self.episodic_memory)} experiences from memory")
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")

        semantic_path = self.storage_path / "semantic_memory.json"
        if semantic_path.exists():
            try:
                with open(semantic_path, 'r') as f:
                    self.semantic_memory = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load semantic memory: {e}")


# =============================================================================
# LEARNING LOOP
# =============================================================================

class LearningLoop:
    """
    The core continuous learning loop.

    This is THE MISSING PIECE that makes Eudaimon AI conscious.

    Loop:
    1. OBSERVE: Gather data from environment
    2. PREDICT: Make predictions about outcomes
    3. ACT: Take action based on prediction
    4. EVALUATE: Compare prediction to outcome
    5. LEARN: Update models based on error
    6. REFLECT: Extract higher-level patterns
    7. THEORIZE: Generate new theories
    8. REPEAT
    """

    def __init__(
        self,
        memory: ExperienceMemory,
        theory_store: Optional['TheoryStore'] = None,
        learning_rate: float = 0.01,
        curiosity_weight: float = 0.3,
        exploration_rate: float = 0.1
    ):
        self.memory = memory
        self.theory_store = theory_store
        self.learning_rate = learning_rate
        self.curiosity_weight = curiosity_weight
        self.exploration_rate = exploration_rate

        # Consciousness state
        self.consciousness = ConsciousnessState(
            level=ConsciousnessLevel.ADAPTIVE,
            learning_mode=LearningMode.OBSERVATION,
            confidence=0.5,
            curiosity=0.5,
            certainty=0.5,
            coherence=0.8,
            attention_focus="initialization",
            active_theories=[],
            recent_insights=[]
        )

        # Learning metrics
        self.total_iterations = 0
        self.prediction_errors: deque = deque(maxlen=1000)
        self.rewards: deque = deque(maxlen=1000)
        self.learning_curve: List[Dict] = []

        # Model registry (for updating)
        self.models: Dict[str, Any] = {}
        self.model_performance: Dict[str, List[float]] = defaultdict(list)

        # Callbacks
        self.on_learn: List[Callable] = []
        self.on_insight: List[Callable] = []
        self.on_theory: List[Callable] = []

    async def run_iteration(
        self,
        context: Dict,
        decision: Dict,
        prediction: Dict
    ) -> Experience:
        """
        Run one iteration of the learning loop.

        This should be called AFTER every prediction/decision.

        Args:
            context: Current market/environment context
            decision: The decision that was made
            prediction: What was predicted to happen

        Returns:
            Experience object (to be updated with outcome later)
        """
        # Create experience (outcome TBD)
        experience = Experience(
            id=self._generate_id(),
            timestamp=datetime.now(),
            context=context,
            decision=decision,
            prediction=prediction,
            outcome={},  # To be filled in
            reward=0.0,
            surprise=0.0,
            tags=self._extract_tags(context, decision),
            importance=1.0
        )

        # Store in working memory
        self.memory.working_memory.append(experience)

        return experience

    async def record_outcome(
        self,
        experience: Experience,
        outcome: Dict,
        user_feedback: Optional[str] = None
    ) -> None:
        """
        Record the outcome of a prediction.

        This completes the experience and triggers learning.

        Args:
            experience: The experience to update
            outcome: What actually happened
            user_feedback: Optional user correction/feedback
        """
        # Update experience
        experience.outcome = outcome
        experience.user_feedback = user_feedback

        # Calculate reward and surprise
        experience.reward = self._calculate_reward(
            experience.prediction,
            outcome,
            user_feedback
        )
        experience.surprise = self._calculate_surprise(
            experience.prediction,
            outcome
        )

        # Update importance based on surprise (surprising = important)
        experience.importance = 1.0 + experience.surprise

        # If user feedback, treat as correction - VERY important
        if user_feedback:
            experience.importance *= 2.0
            experience.lessons_learned.append(f"User correction: {user_feedback}")

        # Store in long-term memory
        self.memory.store(experience)

        # Update metrics
        self.prediction_errors.append(experience.surprise)
        self.rewards.append(experience.reward)
        self.total_iterations += 1

        # LEARN from this experience
        await self._learn_from_experience(experience)

        # Periodically reflect
        if self.total_iterations % 10 == 0:
            await self._reflect()

        # Periodically generate theories
        if self.total_iterations % 50 == 0:
            await self._theorize()

        # Update consciousness state
        self._update_consciousness()

        # Record learning curve
        self.learning_curve.append({
            'iteration': self.total_iterations,
            'avg_error': np.mean(self.prediction_errors),
            'avg_reward': np.mean(self.rewards),
            'consciousness_level': self.consciousness.level.value,
            'timestamp': datetime.now().isoformat()
        })

    async def _learn_from_experience(self, experience: Experience) -> None:
        """
        Learn from a single experience.

        This is where model updates happen.
        """
        # Extract lessons
        lessons = []

        # Lesson from prediction error
        if experience.surprise > 0.5:
            lessons.append(f"High prediction error ({experience.surprise:.2f}): Review {experience.decision}")

        # Lesson from reward
        if experience.reward < 0:
            lessons.append(f"Negative outcome: Avoid similar context {experience.context.get('ticker', 'unknown')}")
        elif experience.reward > 0.5:
            lessons.append(f"Positive outcome: Reinforce {experience.decision}")

        # Lesson from user feedback
        if experience.user_feedback:
            lessons.append(f"User insight: {experience.user_feedback}")

        experience.lessons_learned.extend(lessons)

        # Update relevant models
        for model_name, model in self.models.items():
            if hasattr(model, 'update'):
                try:
                    model.update(experience)
                    self.model_performance[model_name].append(experience.reward)
                except Exception as e:
                    logger.error(f"Failed to update model {model_name}: {e}")

        # Trigger callbacks
        for callback in self.on_learn:
            try:
                callback(experience)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    async def _reflect(self) -> None:
        """
        Reflect on recent experiences to extract patterns.

        This is higher-level learning.
        """
        self.consciousness.learning_mode = LearningMode.REFLECTION

        # Get recent experiences
        recent = list(self.memory.working_memory)

        if len(recent) < 5:
            return

        # Find patterns in recent experiences
        insights = []

        # Pattern: Consistent errors in specific context
        tag_errors = defaultdict(list)
        for exp in recent:
            for tag in exp.tags:
                tag_errors[tag].append(exp.surprise)

        for tag, errors in tag_errors.items():
            if len(errors) >= 3:
                avg_error = np.mean(errors)
                if avg_error > 0.5:
                    insights.append(
                        f"Consistently high errors ({avg_error:.2f}) for '{tag}' - need model improvement"
                    )

        # Pattern: Successful strategies
        positive_exps = [e for e in recent if e.reward > 0]
        if len(positive_exps) >= 3:
            common_context = self._find_common_patterns(positive_exps)
            if common_context:
                insights.append(
                    f"Successful pattern identified: {common_context}"
                )

        # Pattern: Lessons from user corrections
        corrections = [e for e in recent if e.user_feedback]
        if corrections:
            for c in corrections:
                insights.append(f"Learning from user: {c.user_feedback}")

        # Update consciousness with insights
        self.consciousness.recent_insights = insights[-5:]  # Keep last 5

        # Trigger callbacks
        for insight in insights:
            for callback in self.on_insight:
                try:
                    callback(insight)
                except Exception as e:
                    logger.error(f"Insight callback error: {e}")

        # Update semantic memory with patterns
        for tag in tag_errors.keys():
            self.memory.extract_pattern(tag)

    async def _theorize(self) -> None:
        """
        Generate new theories from accumulated experience.

        This is the creative part - hypothesis generation.
        """
        self.consciousness.learning_mode = LearningMode.THEORY_GENERATION

        if not self.theory_store:
            return

        # Get successful patterns
        positive_exps = self.memory.recall_by_outcome(positive=True, top_k=20)

        if len(positive_exps) < 5:
            return

        # Find common patterns in successful experiences
        common = self._find_common_patterns(positive_exps)

        if common:
            # Generate theory
            theory = Theory(
                id=self._generate_id(),
                name=f"Theory_{datetime.now().strftime('%Y%m%d_%H%M')}",
                description=f"Auto-generated theory from {len(positive_exps)} successful experiences",
                hypothesis=f"When {common}, positive outcomes are more likely",
                supporting_evidence=[exp.to_dict() for exp in positive_exps[:5]],
                contradicting_evidence=[],
                confidence=0.6,  # Start with medium confidence
                created_at=datetime.now(),
                tags=['auto_generated']
            )

            self.theory_store.add_theory(theory)
            self.consciousness.active_theories.append(theory.name)

            # Trigger callbacks
            for callback in self.on_theory:
                try:
                    callback(theory)
                except Exception as e:
                    logger.error(f"Theory callback error: {e}")

    def _calculate_reward(
        self,
        prediction: Dict,
        outcome: Dict,
        user_feedback: Optional[str]
    ) -> float:
        """Calculate reward from prediction vs outcome"""
        reward = 0.0

        # Prediction accuracy reward
        if 'expected_return' in prediction and 'actual_return' in outcome:
            error = abs(prediction['expected_return'] - outcome['actual_return'])
            reward = 1.0 - min(1.0, error)  # 0-1 based on accuracy

        # Direction correctness
        if 'direction' in prediction and 'actual_direction' in outcome:
            if prediction['direction'] == outcome['actual_direction']:
                reward += 0.5

        # User feedback bonus
        if user_feedback:
            if 'correct' in user_feedback.lower() or 'good' in user_feedback.lower():
                reward += 0.3
            elif 'wrong' in user_feedback.lower() or 'bad' in user_feedback.lower():
                reward -= 0.5

        return max(-1.0, min(1.0, reward))

    def _calculate_surprise(
        self,
        prediction: Dict,
        outcome: Dict
    ) -> float:
        """Calculate surprise (prediction error magnitude)"""
        if 'expected_return' in prediction and 'actual_return' in outcome:
            return abs(prediction['expected_return'] - outcome['actual_return'])

        if 'confidence' in prediction:
            # If we were confident and wrong, high surprise
            confidence = prediction['confidence']
            was_correct = prediction.get('direction') == outcome.get('actual_direction')
            if was_correct:
                return 1.0 - confidence
            else:
                return confidence

        return 0.5  # Default moderate surprise

    def _extract_tags(self, context: Dict, decision: Dict) -> List[str]:
        """Extract relevant tags from context and decision"""
        tags = []

        if 'ticker' in context:
            tags.append(f"ticker:{context['ticker']}")

        if 'sector' in context:
            tags.append(f"sector:{context['sector']}")

        if 'action' in decision:
            tags.append(f"action:{decision['action']}")

        if 'thesis' in context:
            tags.append(f"thesis:{context['thesis'][:30]}")

        return tags

    def _find_common_patterns(self, experiences: List[Experience]) -> str:
        """Find common patterns in a list of experiences"""
        if not experiences:
            return ""

        # Count tag occurrences
        tag_counts = defaultdict(int)
        for exp in experiences:
            for tag in exp.tags:
                tag_counts[tag] += 1

        # Find tags present in >50% of experiences
        threshold = len(experiences) / 2
        common_tags = [tag for tag, count in tag_counts.items() if count > threshold]

        if common_tags:
            return ", ".join(common_tags)

        return ""

    def _update_consciousness(self) -> None:
        """Update consciousness state based on metrics"""
        # Update confidence based on recent accuracy
        if len(self.prediction_errors) > 0:
            avg_error = np.mean(self.prediction_errors)
            self.consciousness.certainty = max(0, 1.0 - avg_error)

        # Update curiosity based on surprise
        if len(self.prediction_errors) > 0:
            recent_surprises = list(self.prediction_errors)[-10:]
            self.consciousness.curiosity = np.mean(recent_surprises)

        # Update consciousness level based on performance
        if self.total_iterations < 10:
            self.consciousness.level = ConsciousnessLevel.REACTIVE
        elif self.total_iterations < 50:
            self.consciousness.level = ConsciousnessLevel.ADAPTIVE
        elif len(self.consciousness.recent_insights) > 0:
            self.consciousness.level = ConsciousnessLevel.REFLECTIVE

        if len(self.consciousness.active_theories) > 0:
            self.consciousness.level = ConsciousnessLevel.CREATIVE

    def _generate_id(self) -> str:
        """Generate unique ID"""
        data = f"{datetime.now().isoformat()}{np.random.random()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]

    def register_model(self, name: str, model: Any) -> None:
        """Register a model to receive updates"""
        self.models[name] = model

    def get_learning_report(self) -> Dict:
        """Get a report on learning progress"""
        return {
            'total_iterations': self.total_iterations,
            'consciousness_level': self.consciousness.level.name,
            'learning_mode': self.consciousness.learning_mode.value,
            'avg_prediction_error': float(np.mean(self.prediction_errors)) if self.prediction_errors else 0,
            'avg_reward': float(np.mean(self.rewards)) if self.rewards else 0,
            'memory_size': len(self.memory.episodic_memory),
            'active_theories': len(self.consciousness.active_theories),
            'recent_insights': self.consciousness.recent_insights,
            'model_performance': {
                name: np.mean(perf[-100:]) if perf else 0
                for name, perf in self.model_performance.items()
            }
        }


# =============================================================================
# THEORY STORE
# =============================================================================

class TheoryStore:
    """
    Storage and management of AI-generated theories.

    Theories are hypotheses generated from experience patterns.
    They are:
    - Created from successful patterns
    - Tested against new experiences
    - Updated based on evidence
    - Merged or invalidated as needed
    """

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent / "theories"
        self.theories: Dict[str, Theory] = {}
        self._load_theories()

    def add_theory(self, theory: Theory) -> None:
        """Add a new theory"""
        self.theories[theory.id] = theory
        self._save_theories()
        logger.info(f"New theory created: {theory.name}")

    def get_theory(self, theory_id: str) -> Optional[Theory]:
        """Get a theory by ID"""
        return self.theories.get(theory_id)

    def get_active_theories(self) -> List[Theory]:
        """Get all active theories"""
        return [t for t in self.theories.values() if t.status == 'active']

    def test_theory(
        self,
        theory_id: str,
        experience: Experience,
        prediction_correct: bool
    ) -> None:
        """
        Test a theory against an experience.

        Updates theory confidence based on result.
        """
        theory = self.theories.get(theory_id)
        if not theory:
            return

        theory.test_count += 1
        theory.last_tested = datetime.now()

        if prediction_correct:
            theory.success_count += 1
            theory.supporting_evidence.append(experience.to_dict())
            # Increase confidence
            theory.confidence = min(1.0, theory.confidence + 0.05)
        else:
            theory.contradicting_evidence.append(experience.to_dict())
            # Decrease confidence
            theory.confidence = max(0.0, theory.confidence - 0.1)

        # Invalidate if confidence too low
        if theory.confidence < 0.2 and theory.test_count >= 10:
            theory.status = 'invalidated'
            logger.info(f"Theory invalidated: {theory.name}")

        # Validate if confidence high and well-tested
        if theory.confidence > 0.8 and theory.test_count >= 20:
            theory.status = 'validated'
            logger.info(f"Theory validated: {theory.name}")

        self._save_theories()

    def get_relevant_theories(
        self,
        context: Dict,
        top_k: int = 5
    ) -> List[Theory]:
        """Get theories relevant to current context"""
        scored = []

        for theory in self.get_active_theories():
            score = 0

            # Tag overlap
            context_tags = set(context.get('tags', []))
            theory_tags = set(theory.tags)
            overlap = context_tags & theory_tags
            score += len(overlap) * 2

            # Confidence weight
            score *= theory.confidence

            # Recency weight
            if theory.last_tested:
                age = (datetime.now() - theory.last_tested).days
                recency = 1.0 / (1 + age * 0.1)
                score *= recency

            scored.append((score, theory))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in scored[:top_k]]

    def _save_theories(self) -> None:
        """Save theories to disk"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        path = self.storage_path / "theories.json"

        with open(path, 'w') as f:
            json.dump(
                {tid: t.to_dict() for tid, t in self.theories.items()},
                f,
                indent=2
            )

    def _load_theories(self) -> None:
        """Load theories from disk"""
        path = self.storage_path / "theories.json"
        if path.exists():
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    for tid, tdict in data.items():
                        theory = Theory(
                            id=tdict['id'],
                            name=tdict['name'],
                            description=tdict['description'],
                            hypothesis=tdict['hypothesis'],
                            supporting_evidence=tdict['supporting_evidence'],
                            contradicting_evidence=tdict['contradicting_evidence'],
                            confidence=tdict['confidence'],
                            created_at=datetime.fromisoformat(tdict['created_at']),
                            last_tested=datetime.fromisoformat(tdict['last_tested']) if tdict.get('last_tested') else None,
                            test_count=tdict['test_count'],
                            success_count=tdict['success_count'],
                            tags=tdict.get('tags', []),
                            derived_from=tdict.get('derived_from', []),
                            status=tdict.get('status', 'active')
                        )
                        self.theories[tid] = theory
                logger.info(f"Loaded {len(self.theories)} theories")
            except Exception as e:
                logger.error(f"Failed to load theories: {e}")


# =============================================================================
# CONSCIOUS LEARNING SYSTEM - MAIN INTERFACE
# =============================================================================

class ConsciousLearningSystem:
    """
    Main interface for the Conscious Learning System.

    This is the unified interface that Eudaimon AI uses to:
    - Record decisions and outcomes
    - Learn from experience
    - Generate new theories
    - Track its own consciousness state

    Usage:
        system = ConsciousLearningSystem()

        # Before making a prediction
        exp = await system.record_decision(context, decision, prediction)

        # After outcome is known
        await system.record_outcome(exp.id, outcome, user_feedback)

        # Get learning report
        report = system.get_report()
    """

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent / "consciousness"

        # Initialize components
        self.memory = ExperienceMemory(storage_path=self.storage_path / "memory")
        self.theory_store = TheoryStore(storage_path=self.storage_path / "theories")
        self.learning_loop = LearningLoop(
            memory=self.memory,
            theory_store=self.theory_store
        )

        # Pending experiences (waiting for outcome)
        self._pending: Dict[str, Experience] = {}

        logger.info("Conscious Learning System initialized")

    async def record_decision(
        self,
        context: Dict,
        decision: Dict,
        prediction: Dict
    ) -> Experience:
        """
        Record a decision before outcome is known.

        Returns Experience with ID to use when recording outcome.
        """
        exp = await self.learning_loop.run_iteration(context, decision, prediction)
        self._pending[exp.id] = exp
        return exp

    async def record_outcome(
        self,
        experience_id: str,
        outcome: Dict,
        user_feedback: Optional[str] = None
    ) -> None:
        """
        Record outcome for a pending experience.

        This triggers the learning process.
        """
        if experience_id not in self._pending:
            logger.warning(f"Experience {experience_id} not found in pending")
            return

        exp = self._pending.pop(experience_id)
        await self.learning_loop.record_outcome(exp, outcome, user_feedback)

    async def learn_from_user_correction(
        self,
        correction: str,
        context: Optional[Dict] = None
    ) -> None:
        """
        Learn from direct user correction.

        This is for when user says "you were wrong about X".
        """
        exp = Experience(
            id=self.learning_loop._generate_id(),
            timestamp=datetime.now(),
            context=context or {},
            decision={'type': 'user_correction'},
            prediction={},
            outcome={'user_said': correction},
            reward=-0.5,  # Corrections imply we were wrong
            surprise=1.0,  # User corrections are always surprising
            tags=['user_correction'],
            user_feedback=correction,
            lessons_learned=[f"User correction: {correction}"],
            importance=3.0  # Very important
        )

        self.memory.store(exp)
        await self.learning_loop._learn_from_experience(exp)

    def get_relevant_theories(self, context: Dict) -> List[Theory]:
        """Get theories relevant to current context"""
        return self.theory_store.get_relevant_theories(context)

    def get_consciousness_state(self) -> ConsciousnessState:
        """Get current consciousness state"""
        return self.learning_loop.consciousness

    def get_report(self) -> Dict:
        """Get comprehensive learning report"""
        return {
            **self.learning_loop.get_learning_report(),
            'theories_active': len(self.theory_store.get_active_theories()),
            'theories_validated': len([
                t for t in self.theory_store.theories.values()
                if t.status == 'validated'
            ]),
            'pending_decisions': len(self._pending)
        }

    def register_model(self, name: str, model: Any) -> None:
        """Register a model to receive updates during learning"""
        self.learning_loop.register_model(name, model)

    def on_learn(self, callback: Callable[[Experience], None]) -> None:
        """Register callback for when learning occurs"""
        self.learning_loop.on_learn.append(callback)

    def on_insight(self, callback: Callable[[str], None]) -> None:
        """Register callback for when an insight is discovered"""
        self.learning_loop.on_insight.append(callback)

    def on_theory(self, callback: Callable[[Theory], None]) -> None:
        """Register callback for when a new theory is generated"""
        self.learning_loop.on_theory.append(callback)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_conscious_system(storage_path: Optional[str] = None) -> ConsciousLearningSystem:
    """Create a new Conscious Learning System"""
    path = Path(storage_path) if storage_path else None
    return ConsciousLearningSystem(storage_path=path)


async def quick_learn(
    context: Dict,
    decision: Dict,
    prediction: Dict,
    outcome: Dict,
    user_feedback: Optional[str] = None,
    system: Optional[ConsciousLearningSystem] = None
) -> Dict:
    """
    Quick learning from a single experience.

    Use this when you have the outcome immediately.
    """
    if system is None:
        system = ConsciousLearningSystem()

    exp = await system.record_decision(context, decision, prediction)
    await system.record_outcome(exp.id, outcome, user_feedback)

    return system.get_report()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EUDAIMON AI - CONSCIOUS LEARNING SYSTEM")
    print("=" * 60)
    print()
    print("This module provides the MISSING PIECE for conscious AI:")
    print("- Continuous learning from experience")
    print("- Memory of all decisions and outcomes")
    print("- Automatic theory generation")
    print("- Self-correction and improvement")
    print()
    print("Usage:")
    print("  from eudaimon_ai.conscious_learning_system import ConsciousLearningSystem")
    print("  system = ConsciousLearningSystem()")
    print("  exp = await system.record_decision(context, decision, prediction)")
    print("  await system.record_outcome(exp.id, outcome)")
    print()
