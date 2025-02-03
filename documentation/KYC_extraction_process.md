# Process to extract KYC info from policies (LLM-based)
From relevant policy documents we want to extract data to end up with a set of KYC actions and variables related to them.

## Needed steps
1. Identify **sections** that contain requirements in the policy (Matthew)
2. Section ->  **Actions** (aka KOS or requirements) -> **Data points**
    1. Separate sentences (Valeria)
    2. Check if the sentence is an action (Valeria)
    3. Check if the action is KYC relevant (Valeria)
    4. Extract data points from actions (e.g. from action "Collect middle name of senior manager" -> "middle name") -> we already have a template of data points, which may be incomplete (Pulkit)
    5. Verify if more data points emerge from the action (Pulkit)
    6. In case they do, we should add them to the template (Pulkit)
3. Pull out from those actions and data points:
    1. The **variables** (e.g. from "Collect middle name of senior manager" the role should be "middle manager") -> we have a <u>fixed list</u> of needed variables (Alessio)
    2. The **type of evidence** we should request to satisfy that data point (Alessio)
4. **Output CSV** with section numbers, actions, data points and variables  (should be versioned, at least in the filename) (Alessio)
5. **Call the backend** POST route to save document in S3 and map them to database

## TBD - human reiteration loop
An admin should be added in the loop to supervise the steps. This can be modeled an **accept/refuse** UI button after each step 1-4. We need to decide what action the user can take in case they refuse. Current options are:
- change of prompt
- change of generated outputs (which will always be in xlsx format)