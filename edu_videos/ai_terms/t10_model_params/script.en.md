# t10 Model and parameters — narration (English)

v1.3 (2026-11-09, per lines_r3 judges: l16, l37 shorter callback; after voice QA, l24 "a ride of eight kilometers" so the recognizer doesn't abbreviate it to "8km"). v1.2 (2026-11-09, per lines_r2 judges: l10 in calculation order, l14 shorter, l16, l22 "nudge … up", l28, l30 no second "So when", l43 "They're the clue" instead of a third question). v1.1 (2026-11-09, per lines_r1 judges: l08, l14, l22 backs off the per-km knob and nudges the base fare up, l25 "thirty dollars fifty", l26/l27 no longer overlap, l31 dropped (repeat), l33 GPT-3 spelled for TTS, l40 "In short" without repeating l39, l43 calls back the vertical lines). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` (`drafts/v1_en.md`); the author only merged and trimmed lines to match `script.md`, and checked facts (l26 no longer reads out the rounded readings). Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: You've probably seen it in the news: some big AI model has over a hundred billion parameters.
- l02: So what actually is a parameter? And what does it mean to have that many?
- l03: Last time, we saw that today's AI mostly figures out patterns on its own, from examples. What it ends up with is called a model.
- l04: So this time, let's crack a model open and see what's really inside.

## s2 What a model looks like [章:problem]
- l05: A model is basically a machine: you feed an input in one end, and an answer comes out the other.
- l06: And on this machine, there's a row of knobs. Turn them to different positions, and the same input gives a different answer.
- l07: Those knobs are the parameters.
- l08: Here's an example: guessing a taxi fare. We put in the distance in kilometers, and out comes a guess at the price.
- l09: At its simplest, this machine needs just two knobs: one for the base fare, and one for the price per kilometer.
- l10: To make a guess, it multiplies the per-kilometer price by the distance, then adds the base fare.
- l11: Say the base fare is set to {$10|ten dollars} and the per-kilometer knob to {$2|two dollars}. For a {5|five}-kilometer ride, it guesses {$20|twenty dollars}.
- l12: People decide how the machine does its math. But where each knob is set? Nobody types that in. The machine learns it from examples.
- l13: That's all "learning" is: turning the knobs to the right positions.

## s3 Let's turn the knobs [章:experiment]
- l14: Here are twelve made-up taxi rides.
- l15: Each dot is one ride: the further right, the longer the trip, and the higher up, the more it cost.
- l16: Put its guesses on a graph, and the straight line gives you a fare for any distance.
- l17: The little vertical line from each dot to that line shows how far off the guess was for that ride.
- l18: Let's start with the knobs set pretty much at random: {$0|zero} base fare, {$1|a dollar} per kilometer. The line's way too low, and every ride gets underestimated.
- l19: Turn the base fare up to {$10|ten dollars}, and the whole line lifts up.
- l20: Now the short rides are pretty close, but the longer the ride, the further off it gets.
- l21: So turn the per-kilometer knob, and the line gets steeper. At {$3.50|three fifty} a kilometer, we've gone too far: now the long rides are overestimated.
- l22: Back the per-kilometer knob off to about {$2.50|two fifty}, and nudge the base fare up to {$10.20|ten dollars twenty}.
- l23: Now the line runs right along the dots, and all those little vertical lines are short.
- l24: Once it's tuned, you can actually use it. So ask it: what would a ride of {8|eight} kilometers cost?
- l25: None of our twelve rides was eight kilometers, but it can still make a guess: about {$30.50|thirty dollars fifty}.

## s4 What it learned [章:lens]
- l26: So what did this machine actually learn?
- l27: Everything it learned from those twelve rides comes down to where those two knobs are set.
- l28: The machine itself hasn't changed one bit. Only the knob settings have.
- l29: Copy those two numbers onto a scrap of paper, hand it to a friend, and they've got the exact same model.
- l30: When people talk about "training a model," all they're really doing is turning knobs.

## s5 Billions of knobs [章:real]
- l32: Two knobs are plenty for guessing a taxi fare. But if you want a model to write essays or chat with people, you need way, way more.
- l33: In {2020|twenty twenty}, OpenAI released {GPT-3|G P T three}, which has {175 billion|a hundred and seventy-five billion} parameters.
- l34: That's a hundred and seventy-five billion knobs.
- l35: How many is that? Read out one knob setting every second, no eating, no sleeping, and it'd take you over five and a half thousand years.
- l36: Obviously, nobody turned all those knobs by hand. Their settings came from training on huge amounts of text.
- l37: But it's the same idea as the taxi fare: people pick the math, and the settings are learned.
- l38: And a trained model, saved to a file, is mostly just this long, long list of knob settings.
- l39: So when the news says "over a hundred billion parameters," it means the machine has over a hundred billion knobs.

## s6 Wrap-up [包装:outro]
- l40: In short, a model is a machine with knobs.
- l41: And learning just means turning the knobs to the right positions.
- l42: But what does "the right positions" actually mean?
- l43: Remember those little vertical lines, some long, some short? They're the clue.
- l44: That's next time, when we talk about loss functions.
