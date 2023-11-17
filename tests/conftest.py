import os

import pytest
import transformer_lens as tl
from torch.utils.data import DataLoader

from auto_circuit.data import PromptPairBatch, load_datasets_from_json
from auto_circuit.model_utils.micro_model_utils import MicroModel

DEVICE = "cpu"

cfg = tl.HookedTransformerConfig(
    d_vocab=50257,
    n_layers=2,
    d_model=4,  # DON'T SET THIS TO 2 OR LAYERNORM WILL RUIN EVERYTHING
    n_ctx=64,
    n_heads=2,
    d_head=2,
    act_fn="gelu",
    tokenizer_name="gpt2",
    device=DEVICE,
)
mini_tl_model = tl.HookedTransformer(cfg)


def repo_path_to_abs_path(path: str) -> str:
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_path, path)


@pytest.fixture(scope="session")
def mini_tl_transformer() -> tl.HookedTransformer:
    model = mini_tl_model
    model.init_weights()

    model.cfg.use_attn_result = True
    model.cfg.use_split_qkv_input = True
    model.cfg.use_hook_mlp_in = True
    return model


@pytest.fixture(scope="session")
def mini_tl_dataloader() -> DataLoader[PromptPairBatch]:
    _, test_loader = load_datasets_from_json(
        mini_tl_model.tokenizer,
        repo_path_to_abs_path("datasets/mini_prompts.json"),
        device=DEVICE,
        prepend_bos=True,
        batch_size=1,
        train_test_split=[1, 1],
        length_limit=2,
    )
    return test_loader


@pytest.fixture(scope="session")
def greater_than_gpt2_dataloader() -> DataLoader[PromptPairBatch]:
    _, test_loader = load_datasets_from_json(
        mini_tl_model.tokenizer,
        repo_path_to_abs_path("datasets/greater_than_gpt2-small_prompts.json"),
        device=DEVICE,
        prepend_bos=True,
        batch_size=2,
        train_test_split=[2, 2],
        length_limit=4,
    )
    return test_loader


@pytest.fixture(scope="session")
def micro_dataloader(
    multiple_answers: bool = False, batch_count: int = 1, batch_size: int = 1
) -> DataLoader[PromptPairBatch]:
    dataloader_len = batch_size * batch_count
    file_name = f"micro_model_inputs{'_multiple_answers' if multiple_answers else ''}"
    _, test_loader = load_datasets_from_json(
        None,
        repo_path_to_abs_path(f"datasets/{file_name}.json"),
        device=DEVICE,
        prepend_bos=True,
        batch_size=batch_size,
        train_test_split=[dataloader_len, dataloader_len],
        length_limit=dataloader_len * 2,
    )
    return test_loader


@pytest.fixture(scope="session")
def micro_model() -> MicroModel:
    return MicroModel(n_layers=2)
