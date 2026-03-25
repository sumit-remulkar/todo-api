from agents import (
    coder_agent,
    debugger_agent,
    devops_agent,
    planner_agent,
    refactor_agent,
    stack_agent,
    test_agent,
    project_structure_agent
)

from executor import run_project
from executor import test_runner
from utils.github_manager import push_project


class AIController:

    def run(self, prompt):

        plan = planner_agent.create_plan(prompt)

        stack = stack_agent.choose(plan)

        structure = project_structure_agent.generate(stack)

        coder_agent.generate(structure)

        for attempt in range(5):

            print(f"\nAttempt {attempt+1} running project...")

            result = run_project.run()

            if not result.error:
                print("Project running successfully")
                break

            print("Error detected. Fixing with AI...")
            debugger_agent.fix(result.error)

        tests = test_agent.generate()

        test_runner.run_tests()

        refactor_agent.clean()

        devops_agent.generate()

        # 🚀 GitHub Push
        repo_url = push_project(
            repo_name="ai-generated-project",
            project_path="workspace/generated_projects"
        )

        print("Project pushed to GitHub:", repo_url)

        return "Project Generated Successfully"
    