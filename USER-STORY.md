# The user story
*Written 12:30, after Brian Hackett (Replay CEO, judge) said: think hard about the user story and product thinking, and model the pitch on that.*

## Maya

Maya is the only person on a four-person team who cares about QA. There is no QA hire. She ships an internal ops tool that was largely written by a coding agent, and she ships it most Fridays.

Her Friday looks like this. She points Replay at the deploy. It comes back with eight bugs, root-caused, with reproduction steps. She pastes them into her coding agent. They get fixed. She ships.

**Next Friday, she does it again. Eight more bugs. Three of them are the same *kind* of bug she fixed last week**, in different modals, wearing different symptoms. She pays full price, again, to rediscover something she already solved.

And here is the part that matters: **she knows.** She can feel it. She thinks *"we've fixed this three times now."*

Eventually she gets annoyed enough to write it down. A note in `CLAUDE.md`, a lint rule, a comment in the PR. Three sprints later, someone finally patches the prompt.

**Maya is the ratchet.** She is the mechanism that stops the team sliding backwards, and she is doing it by hand, from memory, on top of her actual job. It does not scale past her patience, it does not survive her going on holiday, and it does not leave the building when she solves something every other team is also hitting.

## The one line
> **Ratchet is Maya's instinct, automated and verified.**

## Why this needs AI, not a lint rule
Maya cannot write a rule for *"this modal doesn't reset its state"* that generalises to a modal she has never seen. The three bugs share a root cause but not a selector, not a file, not a symptom. Matching them requires understanding the root cause, not matching a string. That is the whole reason retrieval is semantic.

## What changes for her
- She stops paying to rediscover. Same class, second time: one step, not four.
- The knowledge stops living in her head. It lives somewhere her agent reads automatically, next Friday, without her remembering to.
- **Her fix stops being hers.** Verified and published, it makes the *first* run cheap for a team she has never met, who were about to hit the same thing.

## The turn (use this to move from her to the numbers)
> "Every team has a Maya. She's expensive, she's the bottleneck, and Gartner says by 2028 AI coding cost per developer will exceed that developer's salary. Pioneer makes every call cheaper. We delete the call."

## Tradeoffs, said out loud (judges reward named ones)
One target app, not arbitrary repos. Fixture fallbacks behind every integration so the demo cannot die. Five iterations, small n. Feature freeze at 15:00 so the last hour went to making the demo bulletproof instead of adding things.

## If asked "how did you build this in five hours"
Product first, code second. Problem statement and explicit non-goals before any code. A pre-mortem naming five ways the day fails, each with an owned mitigation. An opportunity tree so every feature traced to a real pain. Then a check most hackathon teams skip: *is the problem actually real*, answered with Gartner, CodeRabbit and GitClear data rather than vibes. Then three parallel build lanes with strict file ownership, and a separate session holding the plan and reviewing every diff against the judging criteria. That is why we froze at 15:00 instead of 16:29.
