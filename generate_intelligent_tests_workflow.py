total_jobs = 32
job_prefix = "run_tests_"

print("name: intelligent-tests-pr")
print("on:")
print("  workflow_dispatch:")
print("  pull_request:")
print("    types: [ labeled, opened, synchronize, reopened, review_requested ]")
print()
print("permissions:")
print("  actions: read")
print("jobs:")
print("  display_test_results:")
print("    if: ${{ always() }}")
print("    runs-on: ubuntu-latest")
print("    needs:")

for i in range(1, total_jobs + 1):
    print(f"      - {job_prefix}{i}")
print()
print("    steps:")
print("      - name: Download all test results")
print("        uses: actions/download-artifact@v3")
print()
print("      - name: Combine test results")
print("        run: |")
print(
    '          find . -name "test_results_*.txt" -exec cat {} + >'
    " combined_test_results.txt"
)
print('          echo "Test results summary:"')
print("          cat combined_test_results.txt")
print()
print("      - name: New Failures Introduced")
print("        run: |")
print(
    '          find . -name "new_failures_*.txt" -exec cat {} + >'
    " new_failures_introduced.txt"
)
print('          echo "New Failures Introduced:"')
print("          cat new_failures_introduced.txt")
print()
for i in range(1, total_jobs + 1):
    print(f"  {job_prefix}{i}:")
    print("    runs-on: ubuntu-latest")
    print("    steps:")
    print("      - name: Checkout Ivy 🛎")
    print("        uses: actions/checkout@v2")
    print("        with:")
    print("          path: ivy")
    print("          persist-credentials: false")
    print('          submodules: "recursive"')
    print("          fetch-depth: 100")
    print()
    print("      - name: Determine and Run Tests")
    print("        id: tests")
    print("        run: |")
    print(
        f"          git clone -b master{i} https://github.com/unifyai/Mapping.git"
        " --depth 1"
    )
    print("          pip install pydriller")
    print("          cp Mapping/tests.pbz2 ivy/")
    print("          cd ivy")
    print("          mkdir .ivy")
    print("          touch .ivy/key.pem")
    print("          echo -n ${{ secrets.USER_API_KEY }} > .ivy/key.pem")
    if i == 1:
        print("          python determine_tests.py extra")
    else:
        print("          python determine_tests.py")
    print("          set -o pipefail")
    print(
        f"          python run_tests_pr.py new_failures_{i}.txt | tee"
        f" test_results_{i}.txt"
    )
    print("        continue-on-error: true")
    print()
    print("      - name: Upload test results")
    print("        uses: actions/upload-artifact@v3")
    print("        with:")
    print(f"          name: test_results_{i}")
    print(f"          path: ivy/test_results_{i}.txt")
    print()
    print("      - name: Upload New Failures")
    print("        uses: actions/upload-artifact@v3")
    print("        with:")
    print(f"          name: new_failures_{i}")
    print(f"          path: ivy/new_failures_{i}.txt")
    print()
    print("      - name: Check on failures")
    print("        if: steps.tests.outcome != 'success'")
    print("        run: exit 1")
    print()
