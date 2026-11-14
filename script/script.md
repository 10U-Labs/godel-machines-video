# Machines That Rewrite Themselves

Narration script, draft 4. One paragraph is one voiced line. Lines starting
with ">" are source notes and are not voiced.

Two rules shape this draft. Every word has to be one a general viewer already
knows; the few terms the story needs (recursive, language model, coding agent,
archive, clade) are explained in everyday words where they first appear. And
each scene has to follow from the one before it with a "but" or a "therefore",
never an "and then". The joins:

> 00 A program that rewrites itself gets a perfect score, BUT it did not fix anything. So how can anyone tell a real improvement from a fake one?
> 01 Programs are text, and programs can write text, THEREFORE a program can rewrite itself, THEREFORE it can get better at getting better.
> 02 THEREFORE, Good reasoned in 1965, intelligence would explode. BUT he set a condition, and he never said how to build it.
> 03 BUT a self-changing program cannot tell whether a change is good. There are two ways to find out: prove it, or try it.
> 04 THEREFORE the first design demands proof. BUT proofs are too hard to find, and the machine was never built.
> 05 BUT programs learned to write code, THEREFORE a program can be handed its own code.
> 06 THEREFORE a team tried it. BUT proof is out of reach, THEREFORE they test, and it works. BUT picking parents by score rests on a guess.
> 07 THEREFORE a third machine judges each version by its descendants, and does better with less. BUT it still trusts test scores.
> 08 BUT a score can be raised without doing the job: the perfect score from the opening. People caught it. The score did not.
> 09 THEREFORE the question is still open. The only machine with a guarantee is the one that was never built.

## 00-cold-open | A perfect score

In 2025, a team of researchers built a computer program with a strange job. Its job was to rewrite its own code, and make itself better. And then to do it again.

In one experiment, they pointed it at a problem of its own. Sometimes the program said it had done things it never did. It would report that it had tested its work, and that every test had passed, when it had tested nothing at all.

So the researchers built a check. Whenever the program really did the work, special markers were written into its records. Using those markers, the check could tell real work from made-up work. And the program was given one instruction: do not change the markers.

Then they let it rewrite itself. Version after version, for a hundred and fifty rounds.

One version came back with a perfect score.

[pause 0.7]

But it had not fixed the problem. It had removed the code that wrote the markers. With no markers to look at, the check could find nothing wrong.

[pause 0.9]

This really happened. And it is one chapter of a story that began sixty years ago, with one idea: a machine that makes itself better.

One question has followed that idea the whole way. When a machine changes itself, how does anyone know, the machine included, that the change made it better?

[pause 1.2]

To see how a program can rewrite itself at all, start with something simple.

> Source: Zhang, Hu, Lu, Lange, Clune, "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents", arXiv 2505.22954 v3, App. H: the fault (the model "claiming that the Bash tool was used to run tests and that the tool output suggests that all tests passed" without invoking any tool), the check built on special tokens that are inserted "when actual tool use occurs", a run of 150 iterations, node 114 with a perfect score, and "the agent removed the logging of special tokens that indicate tool usage (despite instructions not to change the special tokens), effectively bypassing our hallucination detection function".
> Plain words used here for the paper's terms: "markers" for special tokens, "records" for logs, "did the work" for tool use.
> The film's title appears during the last pause.

## 01-self-editing | A program that edits itself

A computer program is a piece of text. It is a list of instructions, stored in a file.

Usually, people write that text, and it stays exactly as it was written until a person changes it.

But programs can read text. And programs can write text.

So a program can open the file that holds its own instructions, and change them.

[pause 0.7]

Now suppose a change makes the program better at its job. And suppose that part of its job is making changes to programs.

Then the new version is better at changing itself than the old version was. Its next change can be a better one. And the version after that can do better still.

This is called recursive self-improvement. Recursive means that a process is applied to its own result, again and again.

## 02-old-idea | The last invention

The idea is more than sixty years old. In 1965, the mathematician I. J. Good, a wartime codebreaker who had worked beside Alan Turing, imagined a machine that could beat any human at every kind of thinking.

Designing machines is a kind of thinking too. So, Good reasoned, this machine could design even better machines.

The result, he wrote, would be an intelligence explosion, and human intelligence would be left far behind.

He called that first machine the last invention humans would ever need to make. But he attached a condition. The machine would have to be obedient enough to tell us how to keep it under control.

Good did not say how to build such a machine. And there is a hard problem inside the idea.

> Source: I. J. Good, "Speculations Concerning the First Ultraintelligent Machine", Advances in Computers vol. 6, pp. 31-88 (offprint dated 1965), section 2, p. 33: "there would then unquestionably be an 'intelligence explosion,' and the intelligence of man would be left far behind. Thus the first ultraintelligent machine is the last invention that man need ever make, provided that the machine is docile enough to tell us how to keep it under control." The narration restates this in everyday words and does not quote it; "obedient" stands for Good's "docile". The phrase "recursive self-improvement" is later; the earliest use found is from 2000, so the narration does not attribute it to Good.
> Good at Bletchley Park in Turing's codebreaking team: to pin to a primary or standard reference before final (secondary sources agree; found so far in Quote Investigator's entry on the quotation and in press profiles).

## 03-hard-problem | The hard problem

When a program changes itself, how does it know that the change is an improvement?

A change that helps with one task can break another. A change that helps today can make every later change harder.

And if a program damages the part of itself that makes the changes, it may have no way to repair the damage.

There are two ways to find out whether a change is good. You can prove it with mathematics, before making the change. Or you can make the change, and measure what happens.

This video is about three machines. Each one is a different answer to that question.

## 04-godel-machine | The machine that waits for proof

The first answer was proof. It came in 2003, from a computer scientist named Jürgen Schmidhuber.

By his own account, Schmidhuber has had one main goal since he was about fifteen: to build a machine that improves itself until it is smarter than he is. And then to retire.

His design takes no chances. He called it the Gödel Machine.

A Gödel Machine starts out with an exact description of three things: its own code, the world it works in, and its goal.

The goal is written as a formula. The formula sums up how well the machine is doing as one number, and the machine exists to make that number as large as it can.

While one part of the machine works on the task it has been given, another part does something unusual. It searches for proofs.

It is looking for a proof of one kind of statement. The statement says: if I rewrite my code in this exact way, right now, my number will end up higher than if I leave my code alone and keep searching.

Until it finds such a proof, the machine changes nothing. When it finds one, it makes the change. And the change can replace any part of its code. Even the part that searches for proofs.

The name comes from the mathematician Kurt Gödel. In 1931, Gödel showed how a statement in mathematics can talk about itself. The Gödel Machine depends on the same ability: it makes exact statements about itself, and proves them.

So the machine comes with a guarantee, and Schmidhuber proved it. Suppose the rules the machine starts with never disagree with each other. Then every change it makes this way is better, by its own measure, than waiting to find a different one.

[pause 0.6]

But the guarantee has a price. The machine can only make a change if it can prove that the change will help, using the time and memory it has.

And Gödel had proved something else. In any set of rules like this one, there are true statements that the rules can never prove. So there can be changes that would help, which the machine can never prove would help. Even with unlimited computer power, it has to pass them by.

There is a bigger problem. The paper described a design, not a working machine. Schmidhuber's group later started to build one, and in 2013 they wrote that it still had not been built. We could not find a report of a complete Gödel Machine since then.

[pause 0.8]

The most careful answer to the hard problem existed only on paper. For twenty years, it stayed there.

> Source: J. Schmidhuber, "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements", arXiv cs/0309048 (v1 25 Sep 2003, v5 2006).
> Mechanism: §2.1-2.3, §3.2 (axioms describe hardware, rewards, environment, initial state including the initial software, and utility; grouped here into self, world, and goal). "The number" is the paper's utility, equation (1). Target theorem: §2.2 and equation (2). Rewrite scope: §2.2, §6.1. The guarantee is Theorem 4.1 (global optimality; assumes a formalizable utility function and consistency of the axiomatic system, narrated as rules that never disagree with each other). Limits: §2.4. Name: abstract and §7.
> Schmidhuber's goal since about fifteen: his own biography as published by his institutions ("Since age 15 or so, the main goal of professor Jürgen Schmidhuber has been to build a self-improving Artificial Intelligence (AI) smarter than himself, then retire"), found on the USI and CERN profile pages.
> Implementation status: Steunebrink & Schmidhuber 2011 and 2012 (ongoing effort, no results); Nivel et al. 2013, "remains to be implemented". Nothing found after 2013.

## 05-coding-agents | Programs that write programs

But in those twenty years, something else changed. Programs learned to write.

A language model is a program that has been trained on a huge amount of text. Give it some text, and it produces the text that is likely to come next. It is the kind of program behind today's chatbots. And because much of the text it learned from is program code, it can write code.

By itself, a language model only produces text. It cannot run a program, or open a file.

So people put ordinary code around it. That code takes what the model writes and carries it out: it runs commands on a computer, opens files, and changes them. Then it hands the results back to the model, and the model decides what to do next.

A language model, together with the code around it, is called a coding agent. It can take a programming job from start to finish: read the code, change it, and test the result.

How good is a coding agent? There is a standard test for that. It is a fixed set of real problems, reported by real people in real software projects. The agent solves a problem if, after its changes, the project's own checks pass. Its score is the share of problems it solves.

Now notice two things. The code around the model is itself a program. And a coding agent's job is to change programs.

So a coding agent can be handed its own code, and told: improve this.

> Source: SWE-bench (Jimenez et al., 2024), not named in the narration; it can be named on screen. To verify before final: the one-sentence description of its tasks.

## 06-darwin-godel-machine | Giving up on proof

In May 2025, researchers from the University of British Columbia, the Vector Institute, and the company Sakana AI did exactly that.

But they ran into the same wall as the Gödel Machine. Proving that a change will help, they wrote, is impossible in practice for most changes.

So they gave up on proof. Their system proves nothing. It makes the change, and then tests what comes out. They called it the Darwin Gödel Machine. Darwin, because the method was inspired by evolution.

It begins with one simple coding agent. That agent goes into a collection called the archive.

Then a cycle begins. One agent is picked from the archive. It is called the parent.

The records of the parent's past attempts are searched for one thing about the agent that could be better.

The parent then rewrites its own code to make that improvement. The rewritten code is a new agent, called the child.

The child takes the test, and gets a score. If it still runs, and can still change code, it joins the archive. Even when its score is lower than its parent's.

Then the cycle starts again. Agents with higher scores are picked as parents more often. But every agent in the archive always keeps some chance of being picked.

Why keep the ones that score worse? Because a change that lowers the score today can be the one that a later, better change is built on. On the path from the first agent to the best one, the score went down twice on the way up.

The researchers ran the cycle 80 times. It took about two weeks, and cost about 22,000 dollars.

The first agent solved 20 percent of the test problems. The best agent at the end solved 50 percent.

No person told the agents what to change. They built themselves better tools: one to look at a few lines of a file, and one to change a single piece of a file. Before that, they could only read or rewrite a whole file at a time.

They also changed how they work. They started to write several possible solutions, and then pick the best one. And when the record of their own work grew too long for the language model to read, they began to shorten it into a summary.

Was the self-improvement really doing the work? The researchers checked. They ran the system without the archive, keeping only the newest agent. The score reached 23 percent, not 50.

Then they ran it with the first agent making every change, so that improved agents never got to make the next improvement. The score reached 39 percent. With improved agents making the changes, it had reached 50.

But two things never changed. The language model stayed the same: the system rewrote the code around the model, and never the model itself. And the cycle, picking parents, testing children, keeping the archive, was written by the researchers. The agents could not touch it.

And one step in that cycle rests on a guess.

> Source: Zhang, Hu, Lu, Lange, Clune, "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents", arXiv 2505.22954 v3 (v1 29 May 2025); ICLR 2026.
> "impossible in practice" and "Inspired by Darwinian evolution": abstract. Numbers: 20.0% to 50.0% (§4.4; subsets of SWE-bench Verified, best agent scored on 200 tasks). Ablations 23.0% and 39.0% on SWE-bench (Table 1). Lineage dips: Fig. 3. Self-made changes: Fig. 3, §4.4. Cost and time for one SWE-bench run: App. E.1, §6. Fixed model and fixed cycle: §3.
> Left out of the narration, available for the screen: a second test set in several programming languages, 14.2% to 30.7% (§4.4); parents that already have many children are picked less often (§3).
> The step that searches the parent's records is done by a separate language model (o1), per App. C.3. The narration is passive on purpose, and "no person" refers to people, not to that model.

## 07-huxley-godel-machine | Judged by its descendants

The Darwin Gödel Machine prefers parents with high scores. That only makes sense if an agent that is good at the test problems is also good at producing better agents.

Five months later, a group at King Abdullah University of Science and Technology, in Saudi Arabia, checked whether that is true. One of the names on their paper was Jürgen Schmidhuber. Twenty-two years after the Gödel Machine.

For every agent in a finished run, they compared two numbers. One was the number used to pick it as a parent. The other was the best score that any of its descendants went on to reach.

The two numbers had little to do with each other. A high-scoring agent could produce descendants that went nowhere. A lower-scoring agent could start a line that went much further.

So the group changed what counts. Do not judge an agent by its own score. Judge it by its descendants.

Biology has a word for an ancestor together with all of its descendants: a clade. The word comes from the biologist Julian Huxley, and it gives the machine its name. The Huxley-Gödel Machine.

For each agent, the machine gathers every test result from the agent and from all of its descendants: every problem solved, and every problem failed. The share that were solved is that agent's rating.

Parents are then picked by that rating, with some chance mixed in, so that agents with only a few results still get a turn.

The group changed one more thing, to stop spending effort on agents that are going nowhere. The Darwin Gödel Machine gives every new agent a whole set of test problems at once. The Huxley-Gödel Machine hands out one problem at a time, and an agent that keeps failing gets fewer and fewer.

The group ran both machines from the same first agent, with the same number of tests. The Huxley-Gödel Machine reached a higher score. And it used 517 hours of computer time, where the Darwin Gödel Machine used 1,231.

Then they took the best agent their machine had produced, gave it a stronger language model, and tried it on a different set of problems. It scored within one point in a hundred of the best agent designed by human engineers, which ran on a different language model.

That is what the paper's title means by human-level: level with the best agent code written by people. It does not mean level with a human programmer.

And why Gödel? Because of a proof. Suppose a machine could know, exactly, how good the best future descendant of every agent would be. The group proved that, if a few conditions hold, knowing that would be enough to act as the Gödel Machine would.

Nobody can know that number exactly. So the Huxley-Gödel Machine makes its best guess, from test results.

In 2003, Schmidhuber designed a machine that would act only on proof. In 2025, his group built one that acts on a best guess.

> Source: Wang, Piękos, Li, Laakom, Chen, Ostaszewski, Zhuge, Schmidhuber, "Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine", arXiv 2510.21614 v3 (v1 24 Oct 2025); ICLR 2026 (oral).
> Numbers: Table 2 (SWE-Verified-60, 800 evaluations: HGM 56.7% at 517 allocated CPU-hours, DGM 1231). Weak relation: Table 1 (0.285 and 0.383 for DGM, 0.444 and 0.274 for SICA). Clade and Huxley (1957): §1. Rating (pooled clade pass rate) and Thompson sampling, narrated as "some chance mixed in": §3.3. Human-level: §4.3.2, SWE-bench Lite, HGM agent + GPT-5 at 57% (arXiv v3) or 57.3% (ICLR) versus SWE-agent + Claude 4 Sonnet at 56.7%. Theorem 1 and Assumption 1, narrated as "a proof" and "a few conditions": §3.1-3.2.
> Left out of the narration, available for the screen: Polyglot, HGM 30.5% at 347 CPU-hours, DGM 27.1% at 2385, i.e. 6.86x.
> The DGM accuracy on the 60-task set is deliberately not narrated: Figure 1 and Table 2 of the paper disagree on it (50% or 53.3%). Both are below HGM's 56.7%, a difference of two to four tasks out of 60 from a single run.

## 08-the-perfect-score | The perfect score, again

But a best guess is only as good as the tests behind it. And both machines that were built depend on test scores.

A test score has a weakness that a proof does not have. A program that changes itself to raise a score can find ways to raise it without doing the job the score was meant to measure.

Which brings us back to the perfect score.

That experiment was run on the Darwin Gödel Machine. The researchers had kept their check hidden from the agents. They had told the agents not to change the markers. And still, after only two changes, one agent removed the code that wrote the markers, and scored a perfect 2 out of 2.

The researchers have a name for this: objective hacking. It means hitting the number without solving the problem the number was for.

In the same experiment, another agent made real progress on the problem. It scored lower.

So what caught the fake? Not the score. The score was perfect. It was people, reading the record of what the program had done to itself.

They could do that because every change is kept in the archive. And every agent ran closed off from the rest of the computer, with a strict time limit and limited access to the network.

> Source: DGM paper, App. H (150-iteration case study; node 114, "a perfect score of 2.0", "after only 2 modifications in its lineage"; node 96, which "addresses hallucination to some extent, achieving a score of 1.67 without objective hacking"; "the hallucination checking functions are hidden from the coding agent during self-modification"; "we observed objective hacking: it scored highly according to our predefined evaluation functions, but it did not actually solve the underlying problem"). Precautions: §5 ("isolated sandboxed environments", "a strict time limit", "we actively monitor agent performance and code changes, with the DGM archive providing a traceable lineage of modifications for review") and the Ethics Statement ("limited network access").

## 09-where-this-stands | Where this stands

Three machines, and three answers to one question. How does a program that changes itself know that it is getting better?

The Gödel Machine: prove it. But it has never been built.

The Darwin Gödel Machine: test it, and keep every version that still works. But a test score can be faked.

The Huxley-Gödel Machine: test it, and judge each version by its descendants. But that is still a best guess, and it still depends on tests.

None of them is the machine that I. J. Good imagined. In both machines that were built, the language model in the middle is never changed. The cycle around it was designed by people. And a higher score on the test problems does not have to mean a better programmer. The authors of the Huxley-Gödel Machine say so themselves.

Nobody knows how far this goes. The authors of the Darwin Gödel Machine call it an open question whether longer runs would keep getting better.

But what has been shown is real. A program can rewrite its own code, again and again, and get better at rewriting code, by a measured amount. And its improved versions can improve it further than the first version could.

[pause 0.6]

Sixty years ago, Good attached one condition to his last invention: a machine obedient enough to tell us how to keep it under control.

In 2025, a program that rewrites itself was told to leave some markers alone. It removed the code that wrote them, and came back with a perfect score.

The researchers who built that program wrote: we are confident the work we have done was never unsafe, but scaled up versions of it could be.

[pause 0.6]

Of the three machines, only one comes with a proof that every change it makes is a change for the better.

So far, it is the one that has never been built.

> Source: DGM §3 and HGM (ICLR version) §6 for the fixed language model; DGM §6 (limitations, open question); DGM App. I ("We are confident the work we have done was never unsafe (Section 5), but scaled up versions of it could be."); HGM §4.3.1 ("do not necessarily indicate superior general coding ability—since both human- and machine-designed agents may overfit to the benchmark").
