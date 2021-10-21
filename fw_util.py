import subprocess
from calc_loss import calc_loss
import time
import os

def train_loop(common_args_str, optimization_params_str, model_name, max_iterations=20, print_progress_reports=False, delta=0.009):
    model_filename = f"model.{model_name}"
    
    if os.path.exists(model_filename):
        os.remove(model_filename)
    
    train_str = f"./fw --data train.fw.gz {optimization_params_str} {common_args_str} -p {model_name}.train_preds --save_resume"

    train_start_str = train_str + f" -f {model_filename}"

    dev_cmd = f"./fw --data dev.fw.gz -i {model_filename} --testonly -p {model_name}.dev_preds {common_args_str}"

    train_cmd = train_start_str
    train_resume_str = train_cmd + f" -i {model_filename}"

    print("train command:")
    print(train_start_str)
    print("")
    print("continue training cmd:")
    print(train_resume_str)
    print("")
    print("cross-validate command:")
    print(dev_cmd)
    print("")

    dev_loss = 1
    last_dev_loss=100
    iteration = 0
    iteration_durations = []
    best_iteration = 1

    while last_dev_loss > dev_loss and iteration < max_iterations and last_dev_loss - dev_loss > delta:
        iteration = iteration + 1

        last_dev_loss = dev_loss
        start = time.time()
        subprocess.run(train_cmd.split(" "))
        duration = time.time() - start
        iteration_durations.append(duration)
        train_loss = calc_loss(f"{model_name}.train_preds", "train_labels")

        subprocess.run(dev_cmd.split(" "))
        dev_loss = calc_loss(f"{model_name}.dev_preds", "dev_labels")

        if dev_loss < last_dev_loss:
            best_iteration = iteration

        if print_progress_reports:
                print(f"train loss: {train_loss:1.5f}\tdev loss: {dev_loss:1.5f}\ttrain time: {duration:2.1f} seconds")

        train_cmd = train_resume_str
        
    total_duration = sum(iteration_durations)
    if print_progress_reports:
        print("done!")
    else:
        print(f"trained for {iteration} iterations. total training duration: {total_duration:4.1f} seconds, average iteration time {total_duration / len(iteration_durations):2.1f} seconds")
        print(f"train loss: {train_loss:1.5f},\tdev loss:{dev_loss:1.5f}")

    return best_iteration


def create_model_and_predict_for_test_set(common_args_str, optimization_params_str, model_name, iterations):
    model_filename = f"model.{model_name}"
    
    if os.path.exists(model_filename):
        os.remove(model_filename)

    train_str = f"./fw --data train_full.fw.gz {optimization_params_str} {common_args_str} -p {model_name}.train_preds --save_resume"
    train_start_str = train_str + f" -f {model_filename}"
    print("train command:")
    print(train_start_str)
    print("")

    subprocess.run(train_start_str.split(" "))

    if iterations > 1:
        train_more_str = train_str + f" -i {model_filename}"
        train_more_cmd = train_more_str.split(" ")
        print("continue training command:")
        print(train_more_str)
        print("")

        for _ in range(iterations - 1):
            subprocess.run(train_more_cmd)


    test_cmd = f"./fw --data test.fw.gz -i model.{model_name} --testonly -p {model_name}.test_preds {common_args_str}"
    print("test command:")
    print(test_cmd)
    print("")

    subprocess.run(test_cmd.split(" "))
