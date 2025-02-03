# Process to extract KYC info from policies (LLM-based)
From relevant policy documents we want to extract data to end up with a set of KYC actions and variables related to them.

## Needed steps
1. Identify **sections** that contain requirements in the policy
2. Section ->  **Actions** (aka KOS or requirements) -> **Data points**
    1. Separate sentences
    2. Check if the sentence is an action
    3. Check if the action is KYC relevant
    4. Extract data points from actions (e.g. from action "Collect middle name of senior manager" -> "middle name") -> we already have a template of data points, which may be incomplete
    5. Verify if more data points emerge from the action
    6. In case they do, we should add them to the template
3. Pull out the **variables** from those actions and the datapoint (e.g. from "Collect middle name of senior manager" the role should be "middle manager") -> we have a <u>fixed list</u> of needed variables
4. **Store** excel with section numbers, actions, data points and variables in the database

## TBD - human reiteration loop
An admin should be added in the loop to supervise the steps. This can be modeled an **accept/refuse** UI button after each step 1-4. We need to decide what action the user can take in case they refuse. Current options are:
- change of prompt
- change of generated outputs (which will always be in xlsx format)