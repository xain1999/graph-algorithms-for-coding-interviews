# Graph Algorithms for Coding Interviews — companion code

Tested Python code for the book *Graph Algorithms for Coding Interviews:
100 Solved Problems with Visual Explanations and Python Solutions* by
Mohammed Islam Hadjoudj, founder and CEO of
[LearnGraphTheory.org](https://learngraphtheory.org), who holds a master's
degree in operations research and a BSc in mathematics.

Release **v1.0** matches the **first edition (2026)**. Every listing printed in
the book is included verbatim from this repository, so what you read is
what was tested.

## Run the tests

Python 3.10 or later. The solutions use only the standard library. The
tests also use `pytest` and `networkx` (as an independent reference).

```
pip install -r requirements-dev.txt
cd code
python -m pytest -q
```

The suite checks every book example, edge cases, inputs that must not be
modified, agreement with a brute-force or library reference on hundreds of
random inputs, and inputs near the stated size limits.

A few tests also check running time on inputs near the size limits. Those
depend on the machine, so they carry the `timing` mark and can be left
out:

```
python -m pytest -q -m "not timing"     # correctness only
python -m pytest -q -m timing           # the running-time checks
```

`requirements-dev.txt` accepts any recent pytest and networkx.
`requirements-lock.txt` pins the exact versions this release was tested
with (pytest 9.2.0, networkx 3.4.2), for a reproducible run:

```
pip install -r requirements-lock.txt
```

## Layout

| Folder | Contents |
|---|---|
| `code/solutions/` | One file per approach: the first file listed for each problem below is the one printed in the book, and the others are the approaches the book describes in prose |
| `code/templates/` | The reusable templates of the chapter openers and the Template Index |
| `code/snippets/` | Short snippets from Chapter 2 |
| `code/tests/` | The pytest suite |

To use a solution on an online judge that expects a class method, wrap it:

```python
class Solution:
    def orangesRotting(self, grid):
        return oranges_rotting(grid)
```

## Problem index

| # | Problem | Reference | Files |
|---:|---|---|---|
| 1 | Find if Path Exists in Graph | LeetCode 1971 | `p001_path_exists.py` (also `p001_path_exists_alt.py`) |
| 2 | Find the Town Judge | LeetCode 997 | `p002_town_judge.py` (also `p002_town_judge_brute.py`) |
| 3 | Find Center of Star Graph | LeetCode 1791 | `p003_star_center.py` (also `p003_star_center_alt.py`) |
| 4 | Destination City | LeetCode 1436 | `p004_destination_city.py` (also `p004_destination_city_brute.py`) |
| 5 | Find Champion I | LeetCode 2923 | `p005_find_champion.py` (also `p005_find_champion_rows.py`) |
| 6 | Most Connected Node | original | `p006_most_connected_node.py` (also `p006_most_connected_node_alt.py`, `p006_most_connected_node_brute.py`) |
| 7 | Detect a Cycle in an Undirected Graph | original | `p007_undirected_cycle.py` (also `p007_undirected_cycle_alt.py`, `p007_undirected_cycle_count.py`) |
| 8 | Keys and Rooms | LeetCode 841 | `p008_keys_and_rooms.py` (also `p008_keys_and_rooms_brute.py`) |
| 9 | Number of Provinces | LeetCode 547 | `p009_number_of_provinces.py` (also `p009_number_of_provinces_brute.py`) |
| 10 | Clone Graph | LeetCode 133 | `p010_clone_graph.py` (also `p010_clone_graph_alt.py`) |
| 11 | All Paths From Source to Target | LeetCode 797 | `p011_all_paths.py` (also `p011_all_paths_bfs.py`, `p011_all_paths_memo.py`) |
| 12 | Reorder Routes to Make All Paths Lead to City Zero | LeetCode 1466 | `p012_reorder_routes.py` (also `p012_reorder_routes_alt.py`, `p012_reorder_routes_brute.py`) |
| 13 | Time Needed to Inform All Employees | LeetCode 1376 | `p013_inform_employees.py` (also `p013_inform_employees_alt.py`, `p013_inform_employees_brute.py`) |
| 14 | Evaluate Division | LeetCode 399 | `p014_evaluate_division.py` (also `p014_evaluate_division_brute.py`, `p014_evaluate_division_wide.py`) |
| 15 | Find Champion II | LeetCode 2924 | `p015_find_champion.py` (also `p015_find_champion_brute.py`) |
| 16 | Flood Fill | LeetCode 733 | `p016_flood_fill.py` (also `p016_flood_fill_recursive.py`) |
| 17 | Island Perimeter | LeetCode 463 | `p017_island_perimeter.py` (also `p017_island_perimeter_sides.py`) |
| 18 | Can the Robot Reach the Exit? | original | `p018_robot_exit.py` (also `p018_robot_exit_bfs.py`, `p018_robot_exit_graph.py`) |
| 19 | Number of Islands | LeetCode 200 | `p019_number_of_islands.py` (also `p019_number_of_islands_brute.py`, `p019_number_of_islands_uf.py`) |
| 20 | Max Area of Island | LeetCode 695 | `p020_max_area_island.py` (also `p020_max_area_island_brute.py`, `p020_max_area_island_recursive.py`) |
| 21 | Surrounded Regions | LeetCode 130 | `p021_surrounded_regions.py` (also `p021_surrounded_regions_regions.py`) |
| 22 | Number of Closed Islands | LeetCode 1254 | `p022_closed_islands.py` (also `p022_closed_islands_flag.py`) |
| 23 | Pacific Atlantic Water Flow | LeetCode 417 | `p023_pacific_atlantic.py` (also `p023_pacific_atlantic_brute.py`) |
| 24 | Count Sub Islands | LeetCode 1905 | `p024_sub_islands.py` (also `p024_sub_islands_sink.py`) |
| 25 | Number of Distinct Islands | LeetCode 694 | `p025_distinct_islands.py` (also `p025_distinct_islands_brute.py`, `p025_distinct_islands_path.py`) |
| 26 | Making A Large Island | LeetCode 827 | `p026_large_island.py` (also `p026_large_island_brute.py`) |
| 27 | Longest Increasing Path in a Matrix | LeetCode 329 | `p027_increasing_path.py` (also `p027_increasing_path_brute.py`, `p027_increasing_path_layers.py`, `p027_increasing_path_memo.py`) |
| 28 | Minimum Depth of Binary Tree | LeetCode 111 | `p028_min_depth.py` (also `p028_min_depth_dfs.py`) |
| 29 | Fewest Hops Between Two Nodes | original | `p029_fewest_hops.py` (also `p029_fewest_hops_path.py`) |
| 30 | Shortest Path in Binary Matrix | LeetCode 1091 | `p030_binary_matrix.py` (also `p030_binary_matrix_brute.py`) |
| 31 | Rotting Oranges | LeetCode 994 | `p031_rotting_oranges.py` (also `p031_rotting_oranges_brute.py`) |
| 32 | 01 Matrix | LeetCode 542 | `p032_01_matrix.py` (also `p032_01_matrix_brute.py`, `p032_01_matrix_dp.py`) |
| 33 | Nearest Exit from Entrance in Maze | LeetCode 1926 | `p033_nearest_exit.py` (also `p033_nearest_exit_alt.py`) |
| 34 | Open the Lock | LeetCode 752 | `p034_open_lock.py` (also `p034_open_lock_alt.py`) |
| 35 | Snakes and Ladders | LeetCode 909 | `p035_snakes_ladders.py` (also `p035_snakes_ladders_alt.py`) |
| 36 | Shortest Bridge | LeetCode 934 | `p036_shortest_bridge.py` (also `p036_shortest_bridge_brute.py`) |
| 37 | Jump Game III | LeetCode 1306 | `p037_jump_game.py` (also `p037_jump_game_rec.py`) |
| 38 | Minimum Knight Moves | LeetCode 1197 | `p038_knight_moves.py` (also `p038_knight_moves_brute.py`) |
| 39 | Word Ladder | LeetCode 127 | `p039_word_ladder.py` (also `p039_word_ladder_brute.py`) |
| 40 | Shortest Path in a Grid with Obstacles Elimination | LeetCode 1293 | `p040_obstacles.py` (also `p040_obstacles_alt.py`, `p040_obstacles_brute.py`) |
| 41 | Sliding Puzzle | LeetCode 773 | `p041_sliding_puzzle.py`, `p041_sliding_puzzle_alt.py` (also `p041_sliding_puzzle_brute.py`) |
| 42 | Bus Routes | LeetCode 815 | `p042_bus_routes.py` (also `p042_bus_routes_brute.py`) |
| 43 | Shortest Path Visiting All Nodes | LeetCode 847 | `p043_visit_all_nodes.py` (also `p043_visit_all_nodes_brute.py`) |
| 44 | Is This a Valid Build Order? | original | `p044_build_order.py` (also `p044_build_order_brute.py`) |
| 45 | Course Schedule | LeetCode 207 | `p045_course_schedule.py` (also `p045_course_schedule_brute.py`, `p045_course_schedule_dfs.py`) |
| 46 | Course Schedule II | LeetCode 210 | `p046_course_schedule_ii.py` (also `p046_course_schedule_ii_brute.py`, `p046_course_schedule_ii_dfs.py`) |
| 47 | Find Eventual Safe States | LeetCode 802 | `p047_safe_states.py` (also `p047_safe_states_brute.py`, `p047_safe_states_kahn.py`) |
| 48 | Course Schedule IV | LeetCode 1462 | `p048_course_schedule_iv.py` (also `p048_course_schedule_iv_bits.py`, `p048_course_schedule_iv_brute.py`, `p048_course_schedule_iv_closure.py`) |
| 49 | Find All Possible Recipes from Given Supplies | LeetCode 2115 | `p049_recipes.py` (also `p049_recipes_brute.py`) |
| 50 | Alien Dictionary | LeetCode 269 | `p050_alien_dictionary.py` (also `p050_alien_dictionary_brute.py`, `p050_alien_dictionary_dfs.py`) |
| 51 | Parallel Courses III | LeetCode 2050 | `p051_parallel_courses.py` (also `p051_parallel_courses_brute.py`, `p051_parallel_courses_memo.py`) |
| 52 | Largest Color Value in a Directed Graph | LeetCode 1857 | `p052_color_value.py` (also `p052_color_value_alt.py`, `p052_color_value_brute.py`) |
| 53 | Connectivity Queries | original | `p053_connectivity_queries.py` (also `p053_connectivity_queries_brute.py`) |
| 54 | Number of Connected Components in an Undirected Graph | LeetCode 323 | `p054_count_components.py` (also `p054_count_components_dfs.py`) |
| 55 | Graph Valid Tree | LeetCode 261 | `p055_valid_tree.py` (also `p055_valid_tree_dfs.py`) |
| 56 | Redundant Connection | LeetCode 684 | `p056_redundant_connection.py` (also `p056_redundant_connection_brute.py`) |
| 57 | Accounts Merge | LeetCode 721 | `p057_accounts_merge.py` (also `p057_accounts_merge_brute.py`, `p057_accounts_merge_dfs.py`) |
| 58 | Satisfiability of Equality Equations | LeetCode 990 | `p058_equations.py` (also `p058_equations_brute.py`) |
| 59 | Smallest String With Swaps | LeetCode 1202 | `p059_smallest_swaps.py` (also `p059_smallest_swaps_brute.py`) |
| 60 | Number of Operations to Make Network Connected | LeetCode 1319 | `p060_network.py` (also `p060_network_brute.py`) |
| 61 | Most Stones Removed with Same Row or Column | LeetCode 947 | `p061_most_stones.py` (also `p061_most_stones_brute.py`) |
| 62 | The Earliest Moment When Everyone Become Friends | LeetCode 1101 | `p062_earliest_friends.py` (also `p062_earliest_friends_brute.py`) |
| 63 | Redundant Connection II | LeetCode 685 | `p063_redundant_directed.py` (also `p063_redundant_directed_brute.py`) |
| 64 | Number of Islands II | LeetCode 305 | `p064_islands_ii.py` (also `p064_islands_ii_brute.py`) |
| 65 | Checking Existence of Edge Length Limited Paths | LeetCode 1697 | `p065_limited_paths.py` (also `p065_limited_paths_brute.py`) |
| 66 | Two Teams | original | `p066_two_teams.py` (also `p066_two_teams_brute.py`) |
| 67 | Is Graph Bipartite? | LeetCode 785 | `p067_is_bipartite.py` (also `p067_is_bipartite_brute.py`, `p067_is_bipartite_uf.py`) |
| 68 | Possible Bipartition | LeetCode 886 | `p068_possible_bipartition.py` (also `p068_possible_bipartition_brute.py`, `p068_possible_bipartition_cycle.py`) |
| 69 | Flower Planting With No Adjacent | LeetCode 1042 | `p069_flower_planting.py` (also `p069_flower_planting_brute.py`) |
| 70 | Divide Nodes Into the Maximum Number of Groups | LeetCode 2493 | `p070_max_groups.py` (also `p070_max_groups_brute.py`) |
| 71 | Cheapest Delivery Costs | original | `p071_delivery_costs.py` (also `p071_delivery_costs_brute.py`) |
| 72 | Network Delay Time | LeetCode 743 | `p072_network_delay.py` (also `p072_network_delay_brute.py`) |
| 73 | Path with Maximum Probability | LeetCode 1514 | `p073_max_probability.py` (also `p073_max_probability_brute.py`, `p073_max_probability_log.py`) |
| 74 | Path With Minimum Effort | LeetCode 1631 | `p074_min_effort.py` (also `p074_min_effort_binary.py`, `p074_min_effort_brute.py`, `p074_min_effort_uf.py`) |
| 75 | Cheapest Flights Within K Stops | LeetCode 787 | `p075_cheapest_flights.py` (also `p075_cheapest_flights_alt.py`, `p075_cheapest_flights_brute.py`) |
| 76 | Find the City With the Smallest Number of Neighbors | LeetCode 1334 | `p076_threshold_city.py` (also `p076_threshold_city_alt.py`, `p076_threshold_city_brute.py`) |
| 77 | Number of Ways to Arrive at Destination | LeetCode 1976 | `p077_ways_to_arrive.py` (also `p077_ways_to_arrive_alt.py`, `p077_ways_to_arrive_brute.py`) |
| 78 | Swim in Rising Water | LeetCode 778 | `p078_swim_water.py` (also `p078_swim_water_binary.py`, `p078_swim_water_brute.py`, `p078_swim_water_uf.py`) |
| 79 | Minimum Cost to Make at Least One Valid Path in a Grid | LeetCode 1368 | `p079_min_cost_grid.py` (also `p079_min_cost_grid_brute.py`, `p079_min_cost_grid_dijkstra.py`) |
| 80 | Cheapest Way to Wire the Office | original | `p080_wire_office.py` (also `p080_wire_office_brute.py`) |
| 81 | Min Cost to Connect All Points | LeetCode 1584 | `p081_connect_points.py` (also `p081_connect_points_alt.py`) |
| 82 | Optimize Water Distribution in a Village | LeetCode 1168 | `p082_water_distribution.py` (also `p082_water_distribution_alt.py`, `p082_water_distribution_brute.py`) |
| 83 | Find Critical and Pseudo-Critical Edges in MST | LeetCode 1489 | `p083_critical_edges.py` (also `p083_critical_edges_brute.py`) |
| 84 | Maximum Depth of N-ary Tree | LeetCode 559 | `p084_nary_depth.py` (also `p084_nary_depth_dfs.py`, `p084_nary_depth_rec.py`) |
| 85 | Root the Tree | original | `p085_root_the_tree.py` (also `p085_root_the_tree_rec.py`) |
| 86 | Minimum Height Trees | LeetCode 310 | `p086_min_height_trees.py` (also `p086_min_height_trees_brute.py`) |
| 87 | All Nodes Distance K in Binary Tree | LeetCode 863 | `p087_distance_k.py` (also `p087_distance_k_rec.py`) |
| 88 | Amount of Time for Binary Tree to Be Infected | LeetCode 2385 | `p088_infection_time.py` (also `p088_infection_time_brute.py`) |
| 89 | Tree Diameter | LeetCode 1245 | `p089_tree_diameter.py` (also `p089_tree_diameter_arms.py`, `p089_tree_diameter_brute.py`) |
| 90 | Find Closest Node to Given Two Nodes | LeetCode 2359 | `p090_closest_node.py` (also `p090_closest_node_brute.py`) |
| 91 | Sum of Distances in Tree | LeetCode 834 | `p091_sum_distances.py` (also `p091_sum_distances_brute.py`) |
| 92 | Longest Cycle in a Graph | LeetCode 2360 | `p092_longest_cycle.py` (also `p092_longest_cycle_brute.py`, `p092_longest_cycle_kahn.py`) |
| 93 | Draw It in One Stroke | original | `p093_one_stroke.py` (also `p093_one_stroke_brute.py`) |
| 94 | Minimum Number of Vertices to Reach All Nodes | LeetCode 1557 | `p094_min_vertices.py` (also `p094_min_vertices_brute.py`) |
| 95 | Count Strongly Connected Components | original | `p095_count_scc.py` (also `p095_count_scc_brute.py`, `p095_count_scc_tarjan.py`) |
| 96 | Critical Connections in a Network | LeetCode 1192 | `p096_critical_connections.py` (also `p096_critical_connections_brute.py`) |
| 97 | Minimum Number of Days to Disconnect Island | LeetCode 1568 | `p097_disconnect_island.py` (also `p097_disconnect_island_brute.py`) |
| 98 | Reconstruct Itinerary | LeetCode 332 | `p098_itinerary.py` (also `p098_itinerary_brute.py`) |
| 99 | Valid Arrangement of Pairs | LeetCode 2097 | `p099_valid_arrangement.py` (also `p099_valid_arrangement_brute.py`, `p099_valid_arrangement_smallest.py`) |
| 100 | Cracking the Safe | LeetCode 753 | `p100_crack_safe.py` (also `p100_crack_safe_brute.py`, `p100_crack_safe_greedy.py`) |

## Templates

`bellman_ford.py`, `bfs.py`, `bfs_levels.py`, `bfs_shortest.py`, `bipartite.py`, `bridges.py`, `build_graph.py`, `components.py`, `dfs_iterative.py`, `dfs_recursive.py`, `dijkstra.py`, `floyd_warshall.py`, `grid.py`, `grid_flood.py`, `hierholzer.py`, `kosaraju.py`, `kruskal.py`, `prim.py`, `root_tree.py`, `topo_dfs.py`, `topo_kahn.py`, `union_find.py`, `zero_one_bfs.py`

## Errata and questions

Known corrections are listed in [ERRATA.md](ERRATA.md). To report a new
one, open an issue with the edition, page number and a short description.

## License

The code is released under the MIT License (see [LICENSE](LICENSE)). The
book text and figures are © 2026 Mohammed Islam Hadjoudj, all rights reserved.
LeetCode is a trademark of its respective owner. This project is not
affiliated with LeetCode.
