# Testing Rules for GitHub Stats Animator

## Project Testing Standards

### Directory Structure
- **ALL tests must be placed in `/tests` folder**
- **ALL test results must be written to `/tests/results` folder**
- Use absolute paths for test results to ensure consistency regardless of where scripts are invoked

### Test File Naming
- Test files should be named descriptively: `test_[component]_[feature].py`
- Result files should include timestamp or unique identifier

### Test Coverage Requirements
- Each API endpoint should have comprehensive tests
- Test multiple parameter combinations
- Generate actual SVG outputs for visual verification
- Include edge cases and error scenarios

### Result Organization
- Results should be organized by component/feature
- Include both successful and failed test outputs
- Maintain test logs with timestamps

## Important Notes
- Always use absolute paths for `/tests/results` directory
- Test files should be self-contained and runnable from any location
- Remember these rules across different chat sessions!
