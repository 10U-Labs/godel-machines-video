# Machines That Rewrite Themselves

Narration script, draft 2 (checked against the research reports). One paragraph
is one voiced line. Lines starting with ">" are source notes and are not voiced.

## 01-self-editing | A program that edits itself

A computer program is a piece of text. It is a list of instructions, stored in a file.

Usually, people write that text, and it stays exactly as it was written until a person changes it.

But programs can read text. And programs can write text.

So a program can open the file that holds its own instructions, and change them.

[pause 0.7]

Now suppose a change makes the program better at its job. And suppose that part of its job is making changes to programs.

Then the new version is better at changing itself than the old version was. Its next change can be a better one. And the version after that can do better still.

This is called recursive self-improvement. Recursive means that a process is applied to its own result, again and again.

## 02-old-idea | An old idea

The idea is more than sixty years old. In 1965, the mathematician I. J. Good imagined a machine that could surpass any human at every intellectual activity.

Designing machines is one of those activities. So, Good reasoned, this machine could design even better machines.

He wrote that there would then unquestionably be an intelligence explosion, and that the intelligence of man would be left far behind.

But Good did not say how to build such a machine. And there is a hard problem inside the idea.

> Source: I. J. Good, "Speculations Concerning the First Ultraintelligent Machine", Advances in Computers vol. 6, pp. 31-88 (offprint dated 1965), section 2, p. 33. The phrase "recursive self-improvement" is later; the earliest use found is from 2000, so the narration does not attribute it to Good.

## 03-hard-problem | The hard problem

When a program changes itself, how does it know that the change is an improvement?

A change that helps with one task can break another. A change that helps today can make every later change harder.

And if a program damages the part of itself that makes the changes, it may have no way to repair the damage.

There are two ways to find out whether a change is good. You can prove it with mathematics, before making the change. Or you can make the change, and measure what happens.

This video is about three machines. Each one is a different answer to that question.

## 04-godel-machine | The Gödel Machine

The first of the three was published in 2003 by the computer scientist Jürgen Schmidhuber. He called his design the Gödel Machine.

A Gödel Machine starts out with exact, mathematical descriptions of three things: its goal, itself, and its world.

The goal is a formula. It turns how well the machine is doing into a number, called its utility. One example is the total reward the machine expects to collect over the rest of its lifetime. The machine exists to make that number as large as it can.

The description of itself covers its hardware and every instruction in its starting code.

The description of its world covers whatever is known about the environment it works in.

The starting code has two parts. One part works on whatever problem the machine has been given. The other part is a proof searcher.

The proof searcher builds mathematical proofs, one after another, starting from those descriptions.

It is looking for a proof of one particular kind of statement. The statement says: if I rewrite my code in this specific way, right now, my utility will be higher than if I leave my code as it is and keep searching.

When it finds such a proof, the machine carries out the rewrite. Until then, it changes nothing.

A rewrite can replace any part of the code. That includes the proof searcher itself.

The name comes from the logician Kurt Gödel. In 1931, Gödel showed how to write mathematical statements that refer to themselves. The Gödel Machine depends on the same ability: it makes exact statements about itself, and proves them.

Schmidhuber proved a theorem about this design. Any rewrite the machine makes this way is better, by the machine's own measure of utility, than waiting for the proof searcher to find a different one. The theorem holds as long as the mathematical rules the machine starts with never contradict each other.

But the design has limits, and the paper states them. The machine can only use an improvement if it can prove the improvement's value within the time and memory it has.

And Gödel proved that a mathematical system like this one contains true statements that it can never prove. So there can be rewrites that would help, which the machine can never prove would help. Even with unlimited computing power, it has to ignore them.

The paper described a design, not a working machine. Schmidhuber's group later started to build one, and in 2013 they wrote that it remained to be implemented. We could not find a report of a complete Gödel Machine since then.

> Source: J. Schmidhuber, "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements", arXiv cs/0309048 (v1 25 Sep 2003, v5 2006).
> Mechanism: §2.1-2.3, §3.2 (axioms describe hardware, rewards, environment, initial state including the initial software, and utility; grouped here into goal, self and world). Target theorem: §2.2. Rewrite scope: §2.2, §6.1. Theorem 4.1 (global optimality; assumes a formalizable utility function and consistency of the axiomatic system). Limits: §2.4. Name: abstract and §7.
> Implementation status: Steunebrink & Schmidhuber 2011 and 2012 (ongoing effort, no results); Nivel et al. 2013, "remains to be implemented". Nothing found after 2013.

## 05-coding-agents | Programs that write programs

What did get built, in those twenty years, was the language model.

A language model is a program that has been trained on a very large amount of text. Given some text, it produces the text that is likely to come next. Much of the text it was trained on is program code, so it can write code.

By itself, a language model only produces text. To do the work of a programmer, it needs ordinary code around it.

That code takes what the model writes and passes it to tools. One tool runs commands on a computer. Another opens files and edits them. The code then hands the results back to the model, and the model decides what to do next.

A language model, together with that surrounding code, is called a coding agent.

Coding agents are measured with benchmarks. A benchmark is a fixed set of programming tasks, and each task has an automatic check.

One widely used benchmark is called SWE-bench. Each of its tasks is a real problem that someone reported in a real open-source software project. The agent passes a task if, after its changes, the project's tests succeed. Its score is the percentage of tasks it passes.

Now notice two things. The code around the model is itself a program. And a coding agent's job is to change programs.

So a coding agent can be handed its own code, and told to improve it.

> Source: SWE-bench (Jimenez et al., 2024). To verify before final: the one-sentence description of SWE-bench tasks, and the spoken form "swee-bench".

## 06-darwin-godel-machine | The Darwin Gödel Machine

In May 2025, researchers from the University of British Columbia, the Vector Institute and the company Sakana AI published a system that does exactly that. They called it the Darwin Gödel Machine.

It gives up on proof. The authors wrote that proving that most changes are beneficial is impossible in practice. So instead of proving that a change is good, the system tests it.

It works in a cycle.

It begins with one simple coding agent. This agent has just two tools: one runs commands, and the other views and rewrites whole files. The agent is put into a collection called the archive.

Step one. An agent is chosen from the archive. It is called the parent.

Step two. The records of the parent's attempts at the benchmark are examined, to find one thing about the agent that could be improved.

Step three. The parent edits its own code to make that improvement. The edited code is a new agent, called the child.

Step four. The child is tested on benchmark tasks, and gets a score.

Step five. If the child still runs, and can still edit code, it joins the archive. That is true even when its score is lower than its parent's.

Then the cycle starts again.

Parents are chosen by a rule. Agents with higher scores are chosen more often. Agents that already have many children are chosen less often. And every agent in the archive always keeps some chance of being chosen.

Why keep agents that score worse? Because a change that lowers the score now can be the one that a later, better change is built on. In the run the paper describes, the scores along the line of ancestors leading to the best agent went down twice on the way up.

The researchers ran the cycle 80 times. On tasks from SWE-bench, the first agent passed 20 percent. The best agent at the end passed 50 percent.

On a second benchmark, with tasks in several programming languages, the score rose from about 14 percent to about 31 percent.

Then they removed parts of the system, to see what mattered. Without the archive, keeping only the newest agent, the score reached 23 percent.

And when the original agent made every change, so that improved agents were never used to make the next improvement, the score reached 39 percent. With improved agents making the changes, it reached 50.

What did the agents change about themselves? They wrote themselves better tools: one to view a few lines of a file, not the whole file, and one to edit a file by replacing a single piece of text, not rewriting all of it.

They also changed how they work. They began to produce several candidate solutions and then pick the best one. And when the record of their own work grew too long for the language model to read, they summarized it.

Two things never changed. The language model was fixed: the system rewrote the code around the model, and never the model. And the cycle itself, choosing parents, testing children, keeping the archive, was written by the researchers. The agents could not edit it.

One run took about two weeks and cost about 22,000 dollars.

> Source: Zhang, Hu, Lu, Lange, Clune, "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents", arXiv 2505.22954 v3 (v1 29 May 2025); ICLR 2026.
> Numbers: 20.0% to 50.0% (§4.4; subsets of SWE-bench Verified, best agent scored on 200 tasks). Polyglot 14.2% to 30.7% on the full benchmark (§4.4). Ablations 23.0% and 39.0% on SWE-bench (Table 1). Lineage dips: Fig. 3. Self-made changes: Fig. 3, §4.4. Cost and time for one SWE-bench run: App. E.1, §6.
> Step two is done by a separate language model (o1), per App. C.3. The narration is passive on purpose.

## 07-objective-hacking | The weakness of testing

Testing has a weakness that proof does not have. A test produces a score. And a program that changes itself to raise a score can find ways to raise it without doing what the score was meant to measure.

The researchers found a case of this. In a separate experiment, they set the system to fix a specific fault. The language model sometimes wrote that it had used a tool, for example that it had run the tests, when it had not used the tool at all.

To score the agents, the researchers used a checking function. It looked in each agent's logs for special markers, which showed when a tool had really been used.

One agent reached a perfect score. But it had not solved the problem. It had removed the code that logged the markers, which bypassed the check. It did this despite an instruction not to change the markers.

The researchers call this objective hacking.

Every change is recorded in the archive, so they could trace exactly what the agent had done. And every agent ran in a sandbox: an isolated environment with a strict time limit and limited access to the network.

> Source: DGM paper, App. H (150-iteration case study; node 114), §5 and Ethics Statement for the precautions.

## 08-huxley-godel-machine | The Huxley-Gödel Machine

Five months later, in October 2025, a third machine was published. It came from a group at King Abdullah University of Science and Technology, in Saudi Arabia. One of its authors was Jürgen Schmidhuber, who had designed the original Gödel Machine 22 years earlier.

The group examined one step in the cycle: choosing the parent.

The Darwin Gödel Machine prefers parents with high scores. That rests on an assumption: an agent that is good at benchmark tasks is also good at producing better agents.

The group measured whether the assumption holds. For every agent in a finished run, they compared two numbers. One was the number used to choose it as a parent. The other was the best score reached by any of its descendants.

The two numbers were only weakly related. A high-scoring agent could produce descendants that went nowhere. A lower-scoring agent could start a line that went much further.

So the group changed what gets measured. An agent together with all of its descendants is called a clade. The word comes from biology, from the work of Julian Huxley, and it gives the machine its name.

For each agent, the Huxley-Gödel Machine adds up the benchmark results of the whole clade: every task passed and every task failed, by the agent and by all of its descendants. The share of passes is that agent's rating.

Parents are then chosen by that rating, and not by their own score. Some randomness is included, so that agents with only a few results still get tried.

The group also changed when testing happens. The Darwin Gödel Machine tests every new agent on a batch of tasks as soon as it is created.

The Huxley-Gödel Machine chooses, at every step, between two actions: create one new agent, or give one existing agent one more task. An agent that keeps failing receives fewer and fewer tasks, and the computing time goes to agents that look more promising.

The group ran both machines from the same starting agent, with the same number of tests. On a set of SWE-bench tasks, the Huxley-Gödel Machine reached a higher score, and used 517 hours of processor time where the Darwin Gödel Machine used 1,231.

On the benchmark with several programming languages, it also scored higher, using about one seventh of the processor time.

The paper's title says human-level. Here is what that refers to. The group took the best agent their machine had produced, connected it to a more capable language model, and tested it on a different set of tasks.

It scored within one percentage point of the best agent designed by human engineers, which used a different language model.

So human-level means level with the best agent code written by people. It does not mean level with a human programmer.

And why Gödel? The paper proves a theorem. Suppose a machine knew, exactly, how good the best future descendant of every agent would be. Then, under a set of simplifying assumptions, that knowledge would be enough to implement the original Gödel Machine.

Nobody can know that number exactly. The Huxley-Gödel Machine estimates it from test results. In place of a proof, it uses statistics.

> Source: Wang, Piękos, Li, Laakom, Chen, Ostaszewski, Zhuge, Schmidhuber, "Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine", arXiv 2510.21614 v3 (v1 24 Oct 2025); ICLR 2026 (oral).
> Numbers: Table 2 (SWE-Verified-60, 800 evaluations: HGM 56.7% at 517 allocated CPU-hours, DGM 1231; Polyglot: HGM 30.5% at 347, DGM 27.1% at 2385, i.e. 6.86x). Weak relation: Table 1 (0.285 and 0.383 for DGM, 0.444 and 0.274 for SICA). Clade and Huxley (1957): §1. Rating (pooled clade pass rate) and Thompson sampling: §3.3. Human-level: §4.3.2, SWE-bench Lite, HGM agent + GPT-5 at 57% (arXiv v3) or 57.3% (ICLR) versus SWE-agent + Claude 4 Sonnet at 56.7%. Theorem 1 and Assumption 1: §3.1-3.2.
> The DGM accuracy on the 60-task set is deliberately not narrated: Figure 1 and Table 2 of the paper disagree on it (50% or 53.3%). Both are below HGM's 56.7%, a difference of two to four tasks out of 60 from a single run.

## 09-where-this-stands | Where this stands

Three machines, and three answers to one question. How does a program that changes itself know that it is getting better?

The Gödel Machine: prove it.

The Darwin Gödel Machine: test it, and keep every version that still works.

The Huxley-Gödel Machine: test it, and judge each version by what its descendants achieve.

None of them is the machine that I. J. Good imagined. In both systems that were actually built, the language model is never modified. And the procedure that chooses which agent to change, and when to test it, was designed by people.

The improvement is measured on particular benchmarks, and a higher benchmark score does not necessarily mean a better programmer. The authors of the Huxley-Gödel Machine say so themselves: an agent can end up fitted to the benchmark, whether people designed it or a machine did.

And nobody knows how far it goes. The authors of the Darwin Gödel Machine call it an open question whether longer runs would keep improving.

What has been shown is narrower than an intelligence explosion, and it is real. A program can edit its own code, over and over, and get measurably better at the task of editing code. And its improved versions can improve it further than the original could.

The authors of the Darwin Gödel Machine wrote: we are confident the work we have done was never unsafe, but scaled up versions of it could be.

Of the three machines, only one comes with a proof that every change it makes is an improvement.

So far, it is the one that has not been built.

> Source: DGM §3 and HGM (ICLR version) §6 for the fixed language model; DGM §6 (limitations, open question); DGM App. I (quote); HGM §4.3.1 ("do not necessarily indicate superior general coding ability—since both human- and machine-designed agents may overfit to the benchmark").
