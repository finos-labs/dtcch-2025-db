# KYC ops steps
1. Background check with **x policy for y client** (triggered by KYC-ops) (Matthew + Valeria)
2. Obtain **evidence**. Sources ordered by priority (Matthew + Valeria):
    1. Internal -> from DB with API
    2. Public -> mocked (?)
    3. Client -> provided by users via email
    - Two types of **integrations** (Nikolay):
        1. Internal tools (DB)
        2. Ask client via email (Automated)
    - **[Stage 2 only] Reiteration for extra data points** (e.g. requested full name and passport as evidence, after passport uploaded check the eventual actions that apply to that specific Country and ask for more data)
3. **Identify risk** -> unknown at the moment (Meeka)
4. **Reporting**
    1. Summary of risks
    2. Matrix of risk (True/False)