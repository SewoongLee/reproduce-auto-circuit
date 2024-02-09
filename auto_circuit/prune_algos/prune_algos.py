from dataclasses import dataclass
from functools import partial
from typing import Callable, Dict, List, Optional

from auto_circuit.prune_algos.ACDC import acdc_prune_scores
from auto_circuit.prune_algos.activation_magnitude import (
    activation_magnitude_prune_scores,
)
from auto_circuit.prune_algos.circuit_probing import circuit_probing_prune_scores
from auto_circuit.prune_algos.edge_attribution_patching import (
    edge_attribution_patching_prune_scores,
)
from auto_circuit.prune_algos.ground_truth import ground_truth_prune_scores
from auto_circuit.prune_algos.integrated_edge_gradients import (
    integrated_edge_gradients_prune_scores,
)
from auto_circuit.prune_algos.random_edges import random_prune_scores
from auto_circuit.prune_algos.simple_gradient import simple_gradient_prune_scores
from auto_circuit.prune_algos.subnetwork_probing import subnetwork_probing_prune_scores
from auto_circuit.tasks import Task
from auto_circuit.types import AlgoKey, PruneScores


@dataclass(frozen=True)
class PruneAlgo:
    key: AlgoKey
    name: str
    func: Callable[[Task], PruneScores]
    short_name: Optional[str] = None

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PruneAlgo):
            return False
        return self.name == __value.name and self.func == __value.func


GROUND_TRUTH_PRUNE_ALGO = PruneAlgo(
    key="Official Circuit",
    name="Ground Truth",
    func=ground_truth_prune_scores,
    short_name="GT",
)
# f"PIG ({pig_baseline.name.lower()} Base, {pig_samples} iter)": partial(
#     parameter_integrated_grads_prune_scores,
#     baseline_weights=pig_baseline,
#     samples=pig_samples,
# ),
ACT_MAG_PRUNE_ALGO = PruneAlgo(
    key="Act Mag", name="Activation Magnitude", func=activation_magnitude_prune_scores
)
RANDOM_PRUNE_ALGO = PruneAlgo(
    key="Random", name="Random", short_name="Random", func=random_prune_scores
)
EDGE_ATTR_PATCH_PRUNE_ALGO = PruneAlgo(
    key="Edge Attribution Patching",
    name="Edge Attribution Patching",
    func=edge_attribution_patching_prune_scores,
)
ACDC_PRUNE_ALGO = PruneAlgo(
    key="ACDC",
    name="ACDC",
    func=partial(
        acdc_prune_scores,
        # tao_exps=list(range(-6, 1)),
        tao_exps=[-5],
        tao_bases=[1],
    ),
)
INTEGRATED_EDGE_GRADS_PRUNE_ALGO = PruneAlgo(
    key="Integrated Edge Gradients (Answer Grad)",
    name="Integrated Edge Gradients (Answer Grad)",
    func=partial(
        integrated_edge_gradients_prune_scores,
        samples=50,
    ),
)
INTEGRATED_EDGE_GRADS_LOGIT_DIFF_PRUNE_ALGO = PruneAlgo(
    key="Integrated Edge Gradients (Lop Prob Diff)",
    name="Integrated Edge Gradients",
    short_name="IEG",
    func=partial(
        integrated_edge_gradients_prune_scores,
        samples=50,
        answer_diff=True,
    ),
)
PROB_GRAD_PRUNE_ALGO = PruneAlgo(
    key="Edge Answer Prob Gradient At Clean",
    name="Prob Gradient",
    func=partial(
        simple_gradient_prune_scores,
        grad_function="prob",
        answer_function="avg_val",
        mask_val=0.0,
    ),
)
LOGIT_EXP_GRAD_PRUNE_ALGO = PruneAlgo(
    key="Edge Answer Logit Exp Gradient At Clean",
    name="Exp Logit Gradient",
    func=partial(
        simple_gradient_prune_scores,
        grad_function="logit_exp",
        answer_function="avg_val",
        mask_val=0.0,
    ),
)
LOGPROB_GRAD_PRUNE_ALGO = PruneAlgo(
    key="Edge Answer Log Prob Gradient At Clean",
    name="Logprob Gradient",
    func=partial(
        simple_gradient_prune_scores,
        grad_function="logprob",
        answer_function="avg_val",
        mask_val=0.0,
    ),
)
LOGPROB_DIFF_GRAD_PRUNE_ALGO = PruneAlgo(
    key="Edge Answer Log Prob Diff Gradient At Clean",
    name="Edge Attribution Patching",
    short_name="EAP",
    func=partial(
        simple_gradient_prune_scores,
        grad_function="logprob",
        answer_function="avg_diff",
        mask_val=0.0,
    ),
)  # USE THIS
LOGIT_MSE_GRAD_PRUNE_ALGO = PruneAlgo(
    key="Edge Answer Logit MSE Gradient At Clean",
    name="Logit MSE Gradient",
    short_name="EAP",
    func=partial(
        simple_gradient_prune_scores,
        grad_function="logit",
        answer_function="mse",
        mask_val=0.0,
    ),
)
SUBNETWORK_EDGE_PROBING_PRUNE_ALGO = PruneAlgo(
    key="Subnetwork Edge Probing",
    name="Subnetwork Edge Probing",
    short_name="SEP",
    func=partial(
        subnetwork_probing_prune_scores,
        learning_rate=0.1,
        epochs=2000,
        regularize_lambda=0.5,
        mask_fn="hard_concrete",
        show_train_graph=True,
    ),
)
CIRCUIT_PROBING_PRUNE_ALGO = PruneAlgo(
    key="Circuit Probing",
    name="Circuit Probing",
    func=partial(
        circuit_probing_prune_scores,
        learning_rate=0.1,
        epochs=2000,
        regularize_lambda=0.1,
        mask_fn="hard_concrete",
        show_train_graph=True,
        circuit_sizes=["true_size"],
    ),
    short_name="CP",
)
SUBNETWORK_TREE_PROBING_PRUNE_ALGO = PruneAlgo(
    key="Subnetwork Tree Probing",
    name="Subnetwork Tree Probing",
    short_name="STP",
    func=partial(
        subnetwork_probing_prune_scores,
        learning_rate=0.1,
        epochs=2000,
        regularize_lambda=0.5,
        mask_fn="hard_concrete",
        show_train_graph=True,
        tree_optimisation=True,
    ),
)
CIRCUIT_TREE_PROBING_PRUNE_ALGO = PruneAlgo(
    key="Tree Probing",
    name="Tree Probing",
    func=partial(
        circuit_probing_prune_scores,
        learning_rate=0.1,
        epochs=1000,
        regularize_lambda=0.1,
        mask_fn="hard_concrete",
        show_train_graph=True,
        circuit_sizes=["true_size"],
        tree_optimisation=True,
    ),
    short_name="TP",
)
MSE_CIRCUIT_TREE_PROBING_PRUNE_ALGO = PruneAlgo(
    key="MSE Tree Probing",
    name="MSE Tree Probing",
    short_name="TP",
    func=partial(
        circuit_probing_prune_scores,
        learning_rate=0.1,
        epochs=1000,
        regularize_lambda=0.1,
        mask_fn="hard_concrete",
        show_train_graph=True,
        circuit_sizes=["true_size"],
        tree_optimisation=True,
        faithfulness_target="mse",
    ),
)
OPPOSITE_TREE_PROBING_PRUNE_ALGO = PruneAlgo(
    key="Opposite Tree Probing",
    name="Opposite Tree Probing",
    func=partial(
        circuit_probing_prune_scores,
        learning_rate=0.1,
        epochs=20,
        regularize_lambda=0.1,
        mask_fn="hard_concrete",
        show_train_graph=True,
        circuit_sizes=["true_size", 1000, 10000],
        tree_optimisation=True,
        faithfulness_target="wrong_answer",
    ),
    short_name="OTP",
)

PRUNE_ALGOS: List[PruneAlgo] = [
    GROUND_TRUTH_PRUNE_ALGO,
    ACT_MAG_PRUNE_ALGO,
    RANDOM_PRUNE_ALGO,
    EDGE_ATTR_PATCH_PRUNE_ALGO,
    ACDC_PRUNE_ALGO,
    INTEGRATED_EDGE_GRADS_LOGIT_DIFF_PRUNE_ALGO,
    LOGPROB_GRAD_PRUNE_ALGO,
    LOGPROB_DIFF_GRAD_PRUNE_ALGO,
    LOGIT_MSE_GRAD_PRUNE_ALGO,
    SUBNETWORK_EDGE_PROBING_PRUNE_ALGO,
    CIRCUIT_PROBING_PRUNE_ALGO,
    SUBNETWORK_TREE_PROBING_PRUNE_ALGO,
    CIRCUIT_TREE_PROBING_PRUNE_ALGO,
    MSE_CIRCUIT_TREE_PROBING_PRUNE_ALGO,
    OPPOSITE_TREE_PROBING_PRUNE_ALGO,
]
PRUNE_ALGO_DICT: Dict[AlgoKey, PruneAlgo] = {algo.key: algo for algo in PRUNE_ALGOS}
