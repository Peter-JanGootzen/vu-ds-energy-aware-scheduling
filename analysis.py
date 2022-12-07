import numpy as np
import matplotlib.pyplot as plt
import csv

results_order = {
    "energy" : 0,
    "idle_t" : 1,
    "active_t" : 2,
    "up_t" : 3,
    "exec_t" : 4,
    "makespan_t" : 5,
    "util" : 6,
    "run" : 7
}

metric_label = {
    "energy" : "Energy usage (kWh)"
}

# Inspired by https://stackoverflow.com/a/60270421
def bar_plot(ax, data, policies_names, workload_names, ylabel, colors=None, total_width=0.8, single_width=1, legend=True):
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(zip(policies_names, data)):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])


    ax.set_xticks(range(len(data) + 1))
    ax.set_xticklabels(workload_names)
    ax.set_ylabel(ylabel)
    ax.set_axisbelow(True)
    ax.grid(axis='y')

    # Draw legend if we need
    if legend:
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        ax.legend(bars, policies_names, loc='center right', bbox_to_anchor=(1.25, 0.5))



def read_results(results_path):
    """
        Read results from file path.
    """

    results = np.genfromtxt(results_path, delimiter=',', skip_header=1)
    return results


def get_column_by_metric(results, metric):
    return results[:, results_order[metric]]

def get_avg_metric(results, metric):
    return np.mean(get_column_by_metric(results, metric))

def get_std_metric(results, metric):
    return np.std(get_column_by_metric(results, metric))


def policies_metric(policies_result_paths, policies_names, metric):
    print("---------------------------------------------------------")
    print("The results for each policy showing metric {}".format(metric))
    print("")
    print("{:<12} {:<12} {:<12}".format("POLICY", "AVG", "STD"))
    for policy_result_path, policy_name in zip(policies_result_paths, policies_names): # loop over policies
        results = read_results(policy_result_path)
        metric_avg = get_avg_metric(results, metric)
        metric_std = get_std_metric(results, metric)
        print("{:<12} {:<12.3f} {:<12.3f}".format(policy_name, metric_avg, metric_std))
    print("---------------------------------------------------------")

def policies_workload_metric(policies_workloads_result_paths, policies_names, workload_names, metric):
    print("---------------------------------------------------------")
    print("The results for each policy with each workloads showing metric {}".format(metric))
    print("")
    fmt_string = "{:<12} " + "{:<12} " * len(workload_names)
    print(fmt_string.format("POLICY", *workload_names))
    for policy_workloads_result_paths, policy_name in zip(policies_workloads_result_paths, policies_names): # loop over policies
        policy_results = []
        for policy_workload_path in policy_workloads_result_paths:
            results = read_results(policy_workload_path)
            metric_avg = get_avg_metric(results, metric)
            policy_results += [metric_avg]
        num_workloads = len(policy_workloads_result_paths)
        fmt_string = "{:<12} " + "{:<12.3f} " * len(workload_names)
        print(fmt_string.format(policy_name, *policy_results))
    print("---------------------------------------------------------")

def policies_workloads_barchart(policies_workloads_result_paths, policies_names, workload_names, metric):
    fig, ax = plt.subplots(figsize=(8, 8))

    policies_results = []


    for i, (policy_workloads_result_paths, policy_name) in enumerate(zip(policies_workloads_result_paths, policies_names)): # loop over policies
        policy_results = []
        for policy_workload_path in policy_workloads_result_paths:
            results = read_results(policy_workload_path)
            metric_avg = get_avg_metric(results, metric)
            policy_results += [metric_avg]

        policies_results += [policy_results]

    bar_plot(ax, policies_results, policies_names, workload_names, metric_label[metric])
    plt.savefig("result.pdf")
    plt.show()

# Print single metric (avg + std) for multiple policies
policy_paths = ["experiment1/results1.csv", "experiment1/results2.csv"]
policy_names = ["FCFS", "Random"]
policies_metric(policy_paths, policy_names, "energy")


# Print single metric (avg only) for multiple policies and multiple workloads
policies_workloads_result_paths = [["experiment1/results1.csv", "experiment2/results1.csv", "experiment3/results1.csv"], ["experiment1/results2.csv", "experiment2/results2.csv", "experiment3/results2.csv"]]
policy_names = ["FCFS", "Random"]
workload_names = ["Alibaba", "bitbrains", "Google"]
policies_workload_metric(policies_workloads_result_paths, policy_names, workload_names, "energy")
policies_workloads_barchart(policies_workloads_result_paths, policy_names, workload_names, "energy")



# def make_line_plots(generation_fitness_max, generation_fitness_mean, enemy, algo_num, folder_name='figures'):
#     """
#         Make line plots of max and mean fitness.
#     """
#     mean_means = [np.mean(gen) for gen in generation_fitness_mean]
#     mean_stds  = [np.std(gen)  for gen in generation_fitness_mean]
#     max_means  = [np.mean(gen) for gen in generation_fitness_max]
#     max_stds   = [np.std(gen)  for gen in generation_fitness_max]

#     mean_lows  = [mean_means[i] - mean_stds[i] for i in range(len(mean_means))]
#     mean_highs = [mean_means[i] + mean_stds[i] for i in range(len(mean_means))]
#     max_lows  = [max_means[i] - max_stds[i] for i in range(len(max_means))]
#     max_highs = [max_means[i] + max_stds[i] for i in range(len(max_means))]

#     best_fitness_generations, best_fitness_max = get_ascending_sublist(max_means)

#     generations = np.arange(len(generation_fitness_mean))
#     plt.errorbar(generations, mean_means, yerr=mean_stds, fmt='-o', label='Mean fitness', capsize=5, color='blue')
#     plt.fill_between(generations, mean_lows, mean_highs, color='blue', alpha=0.5)
#     plt.errorbar(generations, max_means,  yerr=max_stds,  fmt='-o', label='Maximum fitness', capsize=5, color='red')
#     plt.fill_between(generations, max_lows, max_highs, color='red', alpha=0.5)
#     plt.plot(best_fitness_generations, best_fitness_max, label='Mean best individual', color='black')
#     plt.xlabel('Generation', fontsize=16)
#     plt.ylabel('Fitness', fontsize=16)
#     plt.title(f'Mean and maximum fitness plotted\nagainst generation for EA {algo_num} and enemy {enemy}',
#               fontsize=22)
#     plt.legend(prop={'size':14})
#     plt.tight_layout()
#     plt.savefig(f'{folder_name}/lineplot_enemy_{enemy}_EA_{algo_num}.pdf', format='pdf', bbox_inches='tight')
#     plt.clf()







