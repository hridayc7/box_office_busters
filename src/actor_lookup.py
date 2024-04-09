from ActorGraph import ActorGraph

# create ActorGraph instance
ag = ActorGraph()

# example usage of lookup_actor_pair(input_graph, actor_a, actor_b, release_year_cutoff)
# lookup_actor_pair returns a list of all movies where both actors have played a role that was released before `release_year_cutoff`
# use `ag.G` as the input graph for the full graph
# you can use actor names or actor ids, whichever is easier (just make sure they're spelled right)
results_with_names = ag.lookup_actor_pair(ag.G, 'Daniel Radcliffe', 'Emma Watson', 2009)

results_with_ids = ag.lookup_actor_pair(ag.G, 4868, 1900, 2009)

print(results_with_names == results_with_ids)

print(results_with_ids)