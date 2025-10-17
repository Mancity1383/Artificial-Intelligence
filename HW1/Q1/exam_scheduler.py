"""
exam_scheduler.py

- Students: fill in the TODO blocks below.
- This code imports test_cases.py and runs on all cases automatically.
- Do NOT modify test_cases.py; implement the missing parts here.

How to use:
> python exam_scheduler.py
"""

from collections import defaultdict
import time
import copy
import test_cases

class ExamSchedulerCSP:
    def __init__(self, courses, students, time_slots):
        """
        :param courses: list of course names (variables)
        :param students: dict mapping student_id -> list of enrolled courses
        :param time_slots: list of available time slots (e.g., [1,2,3])
        """
        self.courses : list = copy.deepcopy(courses)
        self.students : dict = students
        self.time_slots : list = time_slots
        # TODO: create variables list
        self.variables : list = copy.deepcopy(courses)
        # TODO: initialize domains for each course (variable)
        self.domains : dict = self.build_domains()

        # TODO: build conflict graph (constraints) and store in self.conflicts
        # conflicts should be a dict mapping course -> set(of conflicting courses)
        self.conflicts : dict = self.build_constraints()

    def build_domains(self):

        domains = dict()
        for course in self.courses:
                domains[course] =  list(self.time_slots)

        return domains
        
    def build_constraints(self):
        """
        Build and return conflict graph.
        If two courses share any student, they conflict (cannot share same timeslot).
        """
        conflict = dict()

        for course in self.courses:
            conflict[course] = set()
        
        for courses in self.students.values():
            for course in courses:
                for course_2 in courses:
                    if course_2 != course:
                        conflict[course].add(course_2)
                

        # TODO: implement and return a dict mapping course -> set(conflicting_courses)
        return conflict

    def is_consistent(self, assignment : dict, course, value):
        """
        Check if assigning 'value' to 'course' is consistent with current partial assignment.
        Use self.conflicts to check neighbors that already have assignments.

        :param assignment: dict course->timeslot (partial)
        :param course: candidate variable
        :param value: candidate timeslot
        :return: True if no conflict, False otherwise
        """
        # TODO: check for any neighbor in assignment that has same timeslot
        for neighbor in self.conflicts[course]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    # -------------------------
    # Plain Backtracking solver
    # -------------------------
    def backtracking_search(self):
        """Run plain backtracking on this CSP and return an assignment or None."""
        return self._backtrack({})

    def _backtrack(self, assignment):
        # TODO: if assignment is complete return assignment
        if len(assignment) == len(self.courses):
            return assignment
         
        # TODO: select an unassigned variable (naive: first unassigned)
        var = ''
        for v in self.variables:
            if v not in assignment:
                var = v
                break

        if var == '': return None

        # TODO: iterate over domain values for var
        for value in self.domains[var]:
            if self.is_consistent(assignment,var,value):
                assignment[var] = value
                result = self._backtrack(assignment)
                
                if result is not None:
                    return result
                
                assignment.pop(var)


        return None

    # --------------------------------------------
    # Backtracking + MRV + Degree tie-breaker + FC
    # --------------------------------------------
    def select_unassigned_variable(self, assignment : dict , local_domains):
        """
        MRV: choose variable with minimum remaining values (domain size).
        Degree heuristic as a tie-breaker: choose variable with most conflicts (neighbors).
        :param assignment: current partial assignment
        :param local_domains: dict course->list(current_domain_values), used by FC
        :return: selected variable name
        """
        # TODO: implement MRV + Degree tie-breaker

        MRV_set = list()
        min_domain = 9999999
        for items in local_domains:
            if items in assignment.keys():
                continue
            items_len = len(local_domains[items])
            if items_len < min_domain:
                min_domain = len(local_domains[items])
                MRV_set = list()
                MRV_set.append(items)
            elif items_len == min_domain:
                MRV_set.append(items)
        
        if len(MRV_set) > 1 :
            max_conf = -99999
            var = ''
            for item in MRV_set:
                count = 0
                for conflict in self.conflicts[item]:
                    if conflict not in assignment.keys():
                        count +=1
                if max_conf <= count:
                    max_conf = count
                    var = item
            return var
        else:
            return MRV_set.pop()


    def forward_check(self, var, value, assignment, local_domains):
        """
        Remove 'value' from domains of unassigned neighbors (in local_domains).
        Record removed pairs in a list and return (success, removed_list).
        If a neighbor domain becomes empty, return (False, removed_list).
        """
        # TODO: implement forward checking; do not modify self.domains directly.
        record_list = list()

        for neighbor in self.conflicts[var]:
            if neighbor not in assignment.keys():
                if value in local_domains[neighbor]:
                    local_domains[neighbor].remove(value)
                    record_list.append((neighbor,value))
                    if len(local_domains[neighbor]) <= 0 :
                        return False,record_list
        return True, record_list

    def backtracking_with_heuristics(self):
        """Wrapper to run backtracking with MRV + Degree + Forward Checking"""
        # prepare a copy of domains for local manipulation
        local_domains = {v: list(self.domains[v]) for v in self.courses}
        return self._backtrack_heuristic({}, local_domains)

    def _backtrack_heuristic(self, assignment : dict, local_domains):
        # TODO: if assignment complete → return assignment
        if len(assignment) == len(self.courses):
            return assignment
        # TODO: select variable using select_unassigned_variable(assignment, local_domains)
        var = self.select_unassigned_variable(assignment,local_domains)
        # TODO: iterate through values in local_domains[var] (consider ordering)

        for value in local_domains[var]:
            if self.is_consistent(assignment,var,value):
                assignment[var] = value
                status,record_list = self.forward_check(var,value,assignment,local_domains)
                if not status:
                    assignment.pop(var)
                    for var_2,value_2 in record_list:
                            local_domains[var_2].append(value_2)
                else:
                    result = self._backtrack_heuristic(assignment,local_domains)
                    if result is not None:
                        return result
                    
                    assignment.pop(var)
                    for var_2,value_2 in record_list:
                            local_domains[var_2].append(value_2)
        # For each value:
        #   - if consistent, assign
        #   - perform forward_check to prune neighbor domains
        #   - if forward_check OK, recurse with updated local_domains
        #   - restore domains from removed list if recursion fails
        #   - unassign variable and continue



# -------------------------
# Run template on test cases
# -------------------------
if __name__ == "__main__":
    print("Running Exam Scheduling Template on test cases (template has TODOs).")
    for idx, (courses, students, time_slots) in enumerate(test_cases.cases, start=1):
        print("\n=== Test Case", idx, "===")
        print("Courses:", courses)
        print("Students:", students)
        print("Time slots:", time_slots)

        csp = ExamSchedulerCSP(courses, students, time_slots)

        # initialize domains & constraints so student code can assume these exist
        # NOTE: student must implement build_constraints and domain initialization; here we set placeholders
        # TODO (STUDENT): replace the following two lines by proper implementations above
        if csp.domains is None:
            csp.domains = {course: list(time_slots) for course in courses}
        if csp.conflicts is None:
            csp.conflicts = csp.build_constraints()

        print("\n-- Plain Backtracking (student implementation) --")
        start = time.perf_counter()
        sol_plain = csp.backtracking_search()
        end = time.perf_counter()
        print("Solution (plain):", sol_plain)
        print(f"Execution Time: {end - start:.6f} seconds")

        print("\n-- Backtracking + MRV + Degree + Forward Checking (student implementation) --")
        start = time.perf_counter()
        sol_heur = csp.backtracking_with_heuristics()
        end = time.perf_counter()
        print("Solution (heuristic):", sol_heur)
        print(f"Execution Time: {end - start:.6f} seconds")

        print("\n--- End Test Case", idx, "---")
