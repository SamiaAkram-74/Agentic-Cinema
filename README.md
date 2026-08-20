# 🎬 Agentic Cinema

## The Idea

A screenplay tells us **what happens in a story**, but it doesn't automatically tell a production team **how to make it happen**.

A simple line such as:

> *Sarah runs through a crowded street at night.*

can create a long list of production questions:

* Does the location require a permit?
* Is traffic control needed?
* What lighting setup is required?
* How complex will the shoot be?
* Can this scene be grouped with other street scenes?
* How many shooting days might be required?
* What risks should the production team address before filming?

This gap between **storytelling and production planning** inspired us to build **Agentic Cinema**.

Our goal was to create a system that could take a screenplay and transform it into practical production intelligence before filming begins.

---

## What We Built

**Agentic Cinema** is an AI-powered filmmaking production-planning system that converts a screenplay PDF into a structured production plan.

Instead of treating the screenplay as one large document, our system breaks the workflow into specialized stages:

**Screenplay → Script Analysis → Production Planning → Scheduling → Readiness Evaluation → Production Dashboard**

The result is a production-focused view of the screenplay containing:

* Script analysis
* Characters and locations
* Scene information
* Production requirements
* Location complexity
* Permit requirements
* Lighting considerations
* Shooting schedule
* Production readiness score
* Risk register
* Recommended next actions
* AI agent execution trace
* Production Assistant for questions

---

## How It Works

### 1. Upload the Screenplay

A filmmaker uploads a screenplay PDF through our React dashboard.

The frontend sends the file to our FastAPI backend through the `/analyze` endpoint.

The backend validates the file, extracts its contents, processes the agent workflow, and returns the structured production analysis.

The uploaded screenplay is only temporarily handled by the current prototype and is not permanently stored.

---

### 2. Extract the Screenplay

We use **PyPDF** to extract text from the screenplay.

The PDF reader has one focused responsibility: turning the document into plain text.

It does not make production decisions.

This separation allowed us to keep document processing independent from AI reasoning.

---

### 3. Understand the Story

The **Script Analysis Agent** sends the extracted screenplay text to Gemini with a structured prompt.

It identifies important screenplay information such as:

* Title
* Characters
* Locations
* Scenes
* Story summary

The unstructured screenplay is therefore transformed into structured information that the next agents can work with.

---

### 4. Convert Story Information into Production Requirements

The **Production Planning Agent** takes the script analysis and determines what each location may require during production.

For example, an outdoor street location may have:

* High shooting complexity
* Natural lighting
* Permit requirements
* Traffic-control considerations
* Additional production preparation

This is where Agentic Cinema moves beyond simply *understanding the screenplay* and starts thinking about **production requirements**.

---

## Tool-Using Agent Behavior

One of the most important parts of our project is that the system is not simply one chatbot generating one answer.

Different stages have specialized responsibilities, and the assistant can use production tools and structured data.

For example:

**Filmmaker:**
"What are the production requirements for the Street scene?"

The system can:

1. Identify the relevant location.
2. Request the location information.
3. Retrieve deterministic production rules.
4. Combine that information with the production context.
5. Return an actionable explanation.

Our location tool provides stable rules for known locations such as laboratories, streets, and offices.

For unknown locations, the system uses a cautious fallback instead of confidently making assumptions.

This was an important design decision because production requirements should not be silently invented.

---

## Production Data with ClickHouse

We use **ClickHouse** to store structured production records.

Production information can include:

* Movie
* Scene
* Location
* Shooting day
* Complexity
* Permit requirement
* Lighting

This gives the Production Assistant access to project-specific production information instead of relying only on general AI knowledge.

---

## Scheduling the Production

The **Scheduling Agent** uses the screenplay analysis and production plan to generate a shooting schedule.

It considers factors such as:

* Location grouping
* Production complexity
* Required preparation
* Estimated shooting days
* Permit-sensitive locations
* Scene relationships

Grouping scenes by location can potentially reduce unnecessary:

* Travel
* Equipment movement
* Setup changes
* Crew downtime
* Production costs

The result is a more practical view of how the screenplay could be organized for filming.

---

## Production Readiness

We wanted Agentic Cinema to do more than generate a schedule.

So we added a **Production Readiness Evaluator**.

It produces a readiness score out of 100 and identifies areas that should be reviewed before production is locked.

For example:

**Production Readiness: 88/100**

The system can also generate a risk register such as:

* Street location requires a permit
* High-complexity outdoor shooting

And turn those risks into actionable next steps:

* Start permit applications
* Arrange traffic control
* Book a technical location scout
* Prepare a backup lighting plan

This changes the output from simply *information* into **production decision support**.

---

## Production Assistant

Agentic Cinema also includes a **Production Assistant** where filmmakers can ask questions about their project.

For example:

> What are the production requirements for the Street scene?

The assistant can explain that the Street is an outdoor, high-complexity location requiring a permit and natural-light planning, while also highlighting relevant preparation.

The assistant supports two modes.

### Local Mode

Local Mode uses deterministic local production rules and does not require Gemini or ClickHouse.

We made this the default mode so the project remains reliable during demonstrations.

### Live Mode

Live Mode can use Gemini and ClickHouse for AI-powered and project-specific responses.

This mode is explicitly enabled rather than automatically activated when credentials are available.

---

# The Dashboard

We built the frontend using **React, TypeScript, Vite, and Tailwind CSS**.

The dashboard brings the complete workflow into one interface.

It includes:

* Screenplay upload
* Script analysis
* Production plan
* Shooting schedule
* Readiness score
* Risk alerts
* Recommended actions
* Agent execution trace
* Production Assistant
* JSON export
* Print report
* Light and dark themes

The **Agent Trace** is especially important for us.

It shows the processing stages:

1. PDF Reader
2. Script Analysis Agent
3. Production Planning Agent
4. Scheduling Agent
5. Readiness Evaluator

This makes the workflow more transparent and allows users to see that the result comes from multiple specialized stages.

---

# Technology Behind Agentic Cinema

### Backend

* Python
* FastAPI
* Pydantic
* Google Gemini SDK
* PyPDF
* ClickHouse client

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Lucide React

### Database

* ClickHouse

### Testing

* Pytest
* Python compilation checks
* React production build verification
* Browser dashboard testing

Pydantic schemas validate the data exchanged between the different stages, helping prevent malformed AI responses from silently breaking the workflow.

---

# Challenges We Faced

Building an agentic system introduced challenges that a normal single-model application would not necessarily have.

### 1. Turning Unstructured Scripts into Reliable Data

Screenplays are written for humans, not databases.

We needed to transform free-form screenplay text into structured information that later stages could reliably consume.

We addressed this by using structured prompts and Pydantic schemas for validation.

---

### 2. Preventing AI from Making Unsafe Assumptions

Production requirements can vary significantly between locations.

We did not want the system to confidently assume that an unknown location had no permit requirements.

So we created deterministic location rules and a cautious fallback for unknown locations.

This made the system more predictable.

---

### 3. External Service Reliability

Gemini and ClickHouse introduce external dependencies.

During development and demonstrations, depending entirely on external services could make the application slow or unreliable.

We therefore created a **Local Mode** using deterministic production rules.

This means the core demonstration can continue even when external services are unavailable.

---

### 4. Coordinating Multiple Processing Stages

Another challenge was making sure that information produced by one stage could be correctly consumed by the next.

For example:

**Script Analysis → Production Plan → Schedule → Readiness**

A missing scene, malformed AI response, or incomplete production record could affect later stages.

We addressed this through structured schemas, validation, error handling, and fallback behavior.

---

# What We Learned

Building Agentic Cinema taught us that an agentic application is not simply about connecting an LLM to an interface.

The difficult part is designing the **workflow around the model**.

We learned the importance of:

* Giving each agent a clear responsibility
* Separating AI reasoning from deterministic tools
* Validating AI-generated data
* Designing reliable fallbacks
* Using project-specific data alongside AI
* Making agent workflows observable
* Turning AI output into actionable decisions

Most importantly, we learned that the best agentic systems combine **AI reasoning with reliable software engineering** rather than expecting the model to do everything.

---

# Why Agentic Cinema Matters

Pre-production is where many practical decisions need to be made before cameras start rolling.

A missed permit, difficult location, lighting requirement, or scheduling constraint can create problems later.

Agentic Cinema aims to surface these issues earlier.

Instead of starting with:

**"Here is a screenplay."**

we want the production team to be able to start with:

**"Here is what we need to know before we film it."**

Our vision is to make screenplay analysis more useful to the people responsible for actually turning a story into a production.

---

# The Final Result

Agentic Cinema transforms:

**A screenplay PDF**

into:

**Production Intelligence → Schedule → Readiness → Actionable Decisions**

It brings together specialized AI agents, deterministic production tools, structured production data, scheduling, risk analysis, and a filmmaker-facing assistant in one workflow.

Ultimately, **Agentic Cinema is about helping production teams plan faster, identify risks earlier, and make better decisions before filming begins.**

## Steps to Run Agentic Cinema

1. Open the Project in VS Code

2. Start the Backend

Open a VS Code terminal and run:

pip install -r requirements.txt

$env:AGENTIC_CINEMA_LIVE="0"

uvicorn app:app --reload --port 8000

Keep this terminal running.

The backend should be available at:
http://127.0.0.1:8000

3. Start the Frontend

Open a second VS Code terminal and run:

npm install

npm run dev

Keep this terminal running.

4. Open the Application

Open:

http://127.0.0.1:5173

The header should show that the backend is online.


5. Enable Live Gemini and ClickHouse

Local mode is recommended for demonstrations. To use real Gemini and ClickHouse:

$env:AGENTIC_CINEMA_LIVE="1"

uvicorn app:app --reload --port 8000

Your `.env` must contain valid Gemini and ClickHouse credentials.
