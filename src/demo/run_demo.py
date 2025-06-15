# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Demo for AlphaTensor-Quantum.

This demo showcases how to connect the components of AlphaTensor-Quantum with an
existing third-party library, MCTX (https://github.com/google-deepmind/mctx).
MCTX is a package for training and evaluating AlphaZero agents on a variety of
games.

Inspired by the MCTX demo at https://github.com/kenjyoung/mctx_learning_demo,
we use MCTX to build a simplified version of AlphaTensor-Quantum that can run on
a single machine (we strongly recommend access to a GPU to speed up the code).
Despite its simplicity, our demo is able to reproduce the following results of
the AlphaTensor-Quantum paper:
- Best reported T-count for three benchmark targets (Mod 5_4, Barenco Toff 3,
  and NC Toff 3) when running without gadgets (`use_gadgets=False`). This takes
  about 7800 iterations of the training loop on a Nvidia Quadro P1000 GPU.
- Best reported T-count for one benchmark target (Mod 5_4) when running with
  gadgets (`use_gadgets=True`). This takes about 450 iterations on the same GPU.

Our demo is intended to be a starting point for practitioners and researchers to
build on; it is by no means a complete implementation able to reproduce all the
results reported in the AlphaTensor-Quantum paper.

See the repository `README.md` for instructions on how to run the demo.
"""

import time

from absl import app
import jax
import jax.numpy as jnp

import numpy as np
import json
import os

from alphatensor_quantum.src.demo import agent as agent_lib
from alphatensor_quantum.src.demo import demo_config


def main(_):
  # Set up the hyperparameters for the demo.
  config = demo_config.get_demo_config(
      use_gadgets=False  # Set to `False` for an experiment without gadgets.
  )
  exp_config = config.exp_config

  # Initialize the agent and the run state.
  agent = agent_lib.Agent(config)
  run_state = agent.init_run_state(jax.random.PRNGKey(2024))

  best_circuits = [None for _ in config.env_config.target_circuit_types]
  best_returns = [float('inf') for _ in config.env_config.target_circuit_types]
  # Main loop.
  for step in range(
      0, exp_config.num_training_steps, exp_config.eval_frequency_steps
  ):
    time_start = time.time()
    results = agent.run_agent_env_interaction(step, run_state)
    run_state = results["run_state"]
    time_taken = (time.time() - time_start) / exp_config.eval_frequency_steps
    # Keep track of the average return (for reporting purposes). We use a
    # debiased version of `avg_return` that only includes batch elements with at
    # least one completed episode.
    num_games = run_state.game_stats.num_games
    avg_return = run_state.game_stats.avg_return
    actions = run_state.actions
    env_states = run_state.env_states
    demonstration_actions = run_state.demonstrations_actions
    avg_return = jnp.sum(
        jnp.where(
            num_games > 0,
            avg_return / (1.0 - exp_config.avg_return_smoothing ** num_games),
            0.0
        ),
        axis=0
    ) / jnp.sum(num_games > 0, axis=0)
    print(
        f'Step: {step + exp_config.eval_frequency_steps} .. '
        f'Running Average Returns: {avg_return} .. '
        f'Time taken: {time_taken} seconds/step'
    )

    
    # Unpack batched logs from the current result
    log_length = results["actions_log"].shape[0]  # Typically equals eval_frequency_steps
    base_step = step  # This is the starting step of this batch

    # Convert JAX arrays to NumPy arrays
    actions_seq = np.array(results["actions_log"])  # shape (T, B, ...)
    is_terminal_seq = np.array(results["is_terminal_log"])  # shape (T, B)
    init_tensor_index_seq = np.array(results["init_tensor_index_log"])  # shape (T, B)
    change_of_basis_seq = np.array(results["change_of_basis_log"])  # shape (T, B, S, S)

    # Loop through each time step in the batch
    for t in range(log_length):
        step_id = base_step + t  # Actual global step number

        # Package the data for this step
        log_dict = {
            f"step_{step_id}": {
                "actions": actions_seq[t].tolist(),
                "is_terminal": is_terminal_seq[t].tolist(),
                "init_tensor_index": init_tensor_index_seq[t].tolist(),
                "change_of_basis": change_of_basis_seq[t].tolist()
            }
        }

        # Define output file name
        if not os.path.exists("trajectory_logs"):
          os.makedirs("trajectory_logs")
        file_name = f"trajectory_logs/step_{step_id}.json"

        # Save as JSON
        with open(file_name, "w") as f:
            json.dump(log_dict, f)



    # print(f'Actions: {actions}')
    # print(f'Demonstration Actions: {demonstration_actions}')
    # print(f'Env States: {env_states}')
    for t, target_circuit in enumerate(config.env_config.target_circuit_types):
      tcount = int(-run_state.game_stats.best_return[t])
      print(f'  Best T-count for {target_circuit.name.lower()}: {tcount}')



if __name__ == '__main__':
  app.run(main)
