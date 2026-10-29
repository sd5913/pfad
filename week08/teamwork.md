# Week 8: Agile, Scrum and tracking your team's work

The lecture's Agile/Scrum concepts are **quiz material**. This guide connects
them to your group project and shows how to track work using GitHub.
**Execution is 25% of the group-project mark**: small, steady increments and
documented weekly progress. The whole project is 40% of the course grade;
creative idea remains 25% and code remains 50% of its mark.

## 1. Agile: values and principles

The [Agile Manifesto](https://agilemanifesto.org/) was introduced in Week 1.
Its four values favour:

| Value more | Over |
| --- | --- |
| Individuals and interactions | Processes and tools |
| Working software | Comprehensive documentation |
| Customer collaboration | Contract negotiation |
| Responding to change | Following a plan |

The items on the right still have value. For example, working software matters
more than a long report about unfinished software, while a useful README still
helps someone run it. Talk to teammates and intended users, show something
usable, and adjust the plan when evidence changes.

The [twelve principles](https://agilemanifesto.org/principles.html) include early
and frequent delivery, welcoming changing requirements, sustainable development,
technical quality, simplicity and regular reflection on how the team works.

**Iterative** development improves a solution through repeated feedback.
**Incremental** development adds usable pieces that work together. A game might
first support movement, then collecting a star, then sound feedback; a player
test can make you revise any of those interactions.

## 2. Scrum: a framework for learning and delivery

Scrum provides a framework within the wider Agile approach. GitHub Projects is
a tool that can support your work. These are three different concepts.
The [Scrum Guide](https://scrumguides.org/scrum-guide.html) is the primary source
for the definitions below; the linked edition is the 2020 guide.

Scrum's three empirical pillars are:

- **Transparency:** make the work, goals and actual state visible.
- **Inspection:** check progress and results against those goals.
- **Adaptation:** adjust the work or process when you learn something.

### One team, three accountabilities

The guide calls these *accountabilities*; they are often described as roles.
The Scrum Team is self-managing and cross-functional.

| Accountability | Main responsibility |
| --- | --- |
| Product Owner | Maximise product value and order the Product Backlog. |
| Developers | Plan and create usable Increments, maintaining the Definition of Done. |
| Scrum Master | Establish Scrum and help the team improve its effectiveness, including addressing impediments. |

Developers can contribute design, art, testing and other work needed for the
product. The word does not restrict participation to people typing code.

### Artifacts and their commitments

| Artifact | Meaning | Commitment |
| --- | --- | --- |
| Product Backlog | An evolving, ordered list of work needed to improve the product. | Product Goal: the longer-term objective. |
| Sprint Backlog | The Sprint Goal, selected Product Backlog items and an actionable delivery plan. | Sprint Goal: the objective of this Sprint. |
| Increment | A usable, integrated and verified addition to the product. | Definition of Done: the shared quality standard. |

A list of completed tasks is not automatically a usable Increment. Work must
fit together and meet the shared Definition of Done. Multiple Increments can
be delivered during a Sprint; the review meeting is not a release gate.

### The Sprint and its events

A **Sprint** is a fixed-length event of **one month or less**. A new Sprint
starts after the previous one. A one-week cycle can fit your course project.
Keep the Sprint Goal in focus while adapting the delivery plan as you learn.
The following four events happen within the Sprint:

| Event | Purpose |
| --- | --- |
| Sprint Planning | Agree why the Sprint is valuable, what can be Done, and how to deliver it. |
| Daily Scrum | A 15-minute event each working day for Developers to inspect progress toward the Sprint Goal and adapt their plan. |
| Sprint Review | Inspect the product outcome with stakeholders and decide useful future adaptations. |
| Sprint Retrospective | Improve quality and team effectiveness by reflecting on how the work happened. |

Keep **Review** and **Retrospective** distinct: one inspects the product
outcome; the other improves how the team works.

## 3. Track the work in GitHub

[GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
supports table, board and roadmap views of issues and pull requests. Use a
shared board to make plans and progress visible. It supports your process;
creating a board alone does not establish Scrum.

### First, join the course organization and create the shared repository

GitHub supports personal-account Projects too. For this course, keep your
group repository and its board in the [sd5913 organization](https://github.com/sd5913).

1. Accept the organization's invitation while signed into the GitHub account
   you registered at [pfad.ait4x.org](https://pfad.ait4x.org). If it is missing
   or expired, ask the instructor to check your registration and resend it.
2. One teammate creates a **public** repository, choosing **Owner: sd5913** and
   a distinct project name, for example `group-your-project`. You can start from
   an empty repository or one of the course templates. Check the resulting URL
   begins `https://github.com/sd5913/`. If `sd5913` is not an Owner option, check
   that the invitation was accepted before continuing.
3. The repository administrator adds the other teammates with **Write** access
   under **Settings > Collaborators and teams**. Each teammate should check
   they can push a branch. Being an organization member alone does not give
   write access to every course repository.
4. If the team already has a personal repository, ask the instructor to help
   transfer it into `sd5913` and preserve its commits, issues and PRs. Keep the
   project's history instead of starting again; update its local remote and
   Canvas URL after the transfer.

### Then, connect the board, issues and pull requests

1. **Use the course Project template.** Open
   [Group Project 2026](https://github.com/orgs/sd5913/projects/1), click
   **Use this template**, choose **sd5913** as the owner and name the new
   Project after your group project. It includes weekly iterations, a status
   board and dated tutor review cards. Give teammates **Write** access in the Project's
   settings; set this Project's base access for organization members to **Read**
   or **No access** so editing is limited to your group and project
   administrators. Link the Project from your repository's Projects tab and
   README. Project access and
   repository access are separate; check both with a teammate and ensure the
   instructor can view your evidence. Collaborators and repository links are
   not copied from the template, so add them to your new Project.
2. **Create repository issues.** Give each task a concrete outcome, an assignee
   and acceptance checks. For example: "Start button opens the first level";
   check that a teammate can launch the project and use the button.
3. **Add the issues to your Project.** Group the board by Status. A useful set
   is Backlog, Todo, In progress, Review and Done; customize the available status
   options to suit your team. Set priority by ordering work or adding a Priority
   field.
4. **Choose a short goal.** Select work your team can finish together. The
   template's Iteration field has one-week cycles from 29 October to the final
   submission week. Put selected tasks in the relevant iteration; use
   **Current iteration** and **Next iteration** to focus on them. **Team board**
   shows all work and **Delivery dates** shows the full review schedule. Record
   the Sprint Goal and delivery plan too: a status column alone is not a
   complete Sprint Backlog.
5. **Agree your Definition of Done.** For example: integrated with the existing
   project, relevant checks pass, a teammate has tried the interaction, and run
   instructions remain accurate. Issue acceptance checks describe one feature;
   the Definition of Done is the shared quality standard across Increments.
6. **Link the implementation.** Create a branch and PR for the issue. A PR
   description containing `Closes #12` links issue #12 and closes it when the PR
   merges into the repository's **default branch**. Other target branches do
   not trigger this behaviour. Link tests and review observations as evidence.
7. **Keep the board current.** Built-in Project workflows can update Status
   when issues close or PRs merge. Inspect the actual workflow configuration;
   an automatic Done status does not itself check your quality standard.
8. **Record the week's progress.** Briefly note the goal, what became usable,
   review or test evidence, blockers and the next adjustment. Link the board,
   issues, PRs and progress notes from your README.

An illustrative weekly note could be:

```markdown
## Week ending 5 November
Goal: a player can start a level and collect a star.
Completed: issue #12 and PR #18; teammate tested the start button.
Still open: star feedback needs a sound; see issue #13.
What we learned: players missed the first visual cue.
Next change: improve the cue before adding a second level.
```

GitHub is the recommended starting point because your code, issues, reviews and
build results can connect in one place. Trello, Notion or a shared Markdown
task list can also work if the planning and weekly evidence are accessible
from the repository. No additional Canvas upload is needed.

## 4. Weekly delivery meetings with your tutor

Meet your assigned tutor in your scheduled tutorial slot each remaining
teaching week. The dates below identify the **Thursday class weeks**; your
tutor confirms the exact meeting time. The template's dated cards are progress
milestones, not calendar invitations.

| Class week | Bring a usable delivery | Review focus |
| --- | --- | --- |
| 5 November 2026 | First working interaction | Someone can try an input and see a response; agree the next small goal. |
| 12 November 2026 | Integrated core experience | Show the game loop, app flow or installation interaction working together. |
| 19 November 2026 | Playtest and feedback | Bring observations from another person trying the experience; choose an improvement. |
| 26 November 2026 | Delivery candidate | Test a runnable build, deployment or installation setup on your chosen platform. |
| 3 December 2026 | Final tutor delivery review | Rehearse the experience and check the README, access and final fixes. |

Use these focuses to plan a suitable increment for your own project; agree any
scope adjustments with your tutor. At each review, bring the working result,
links to issues/PRs/tests/builds, and a blocker or question. Afterwards, update
the dated card with what works, evidence, tutor feedback and the next goal with
owners. Link the board and these records from your README. If you use another
tracking tool, keep the same dates and an equivalent accessible review record.

The separate **6 December 2026, 23:59 HKT** card is the final Canvas repository
submission deadline, **not a tutor meeting**. Weekly delivery records support
the existing 25% execution criterion; they do not add another grade component
or Canvas upload.

## 5. What the 25% execution criterion looks for

Show small, steady increments and documented weekly progress through:

- Shared planning: ordered tasks, clear ownership and a goal for the next cycle.
- Team contributions that lead to a usable, integrated result.
- Review and test evidence, including feedback and obstacles.
- Reflection and changes to the next plan as the team learns.

The evidence should explain the actual work and decisions. Raw commit counts,
card totals, formal role titles and ceremony attendance are not the grading
criteria. Keep using the same repository through the final deadline; see the
[group-project brief](../assignments/group-project.md).

Computer vision remains optional inspiration for your project. This guide does
not require your team to add a camera feature.

## Sources and revision

- [Agile Manifesto](https://agilemanifesto.org/) and its
  [twelve principles](https://agilemanifesto.org/principles.html).
- [The Scrum Guide, 2020](https://scrumguides.org/scrum-guide.html).
- [GitHub Projects quickstart](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects).
- [GitHub iteration fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields).
- [Linking PRs and issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).
- [Built-in Project automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations).

For revision, explain the four values, iterative versus incremental work, the
three pillars and accountabilities, the artifacts and their commitments, and
the Sprint events. Be able to distinguish a Review from a Retrospective, and a
closed issue from a usable Increment that meets the Definition of Done.
