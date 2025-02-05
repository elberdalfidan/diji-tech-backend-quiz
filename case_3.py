def get_combinations(n, c):
    # n: number of groups (2 < n < 7)
    # c: list of groups (e.g: [['a','b'], ['1','2']])
    
    def combine(groups, current=[]):
        # Base case: If there are no more groups to process, return the current combination
        if not groups:
            return [current]
        
        # Recursive case: Select one element from each group and create combinations
        result = []
        current_group = groups[0]
        remaining_groups = groups[1:]
        
        for item in current_group:
            # Call the recursive function for each element
            new_combinations = combine(remaining_groups, current + [item])
            result.extend(new_combinations)
            
        return result

    # Call the combine function from the main function and return the results
    combinations = combine(c)
    # Convert each combination to a string
    return [''.join(combo) for combo in combinations]


if __name__ == "__main__":
    with open("case_3.txt", "r") as cases_file:
        cases = []
        solutions = []
        for line in cases_file:
            if line.strip():
                c, a = line.strip().split(",")
                cases.append([list(x) for x in c.split("|")])
                solutions.append(a.split("|"))

        for i in range(len(cases)):
            r = get_combinations(len(cases[i]), cases[i])
            a = set("".join(x) for x in r)
            b = set(solutions[i])
            for x in a:
                b.discard(x)
            print(f"Case {i + 1} : {'OK' if len(b) == 0 else 'FAIL'}")
