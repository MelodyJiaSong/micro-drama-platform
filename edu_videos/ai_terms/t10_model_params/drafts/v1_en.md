# t10 Model and parameters — narrator draft (English)

## s0 A hundred billion of what?
- l01: You've probably seen it in the news: some big AI model has more than a hundred billion parameters.
- l02: So what actually is a parameter? And what does it mean to have over a hundred billion of them?
- l03: Last time, we saw that today's AI mostly figures out patterns on its own, from examples.
- l04: And the skill it ends up with is what we call a model.
- l05: So this time, let's crack a model open and see what's really inside.

## s2 What a model looks like
- l06: Honestly, a model is just a machine: you feed an input in one end, and an answer comes out the other.
- l07: And on this machine, there's a row of knobs.
- l08: Turn the knobs to different positions, and the same input gives you a different answer.
- l09: Those knobs are the parameters. Parameters are just knobs.
- l10: Here's an example: guessing a taxi fare.
- l11: What goes in is how many kilometers the ride was, and what comes out is the machine's guess at the price.
- l12: At its very simplest, this machine only needs two knobs: one for the base fare, and one for the price per kilometer.
- l13: To make a guess, it takes the base fare and adds the per-kilometer price times the number of kilometers.
- l14: Say you set the base fare knob to {$10|ten dollars} and the per-kilometer knob to {$2|two dollars}.
- l15: Then for a {5|five}-kilometer ride, it guesses {$20|twenty dollars}.
- l16: Now, how the machine does its math, base fare plus per-kilometer price times distance, is something people decide.
- l17: But where each knob is set? Nobody types that in; the machine has to learn it from examples.
- l18: That's all "learning" is: turning the knobs to the right positions.

## s3 Let's turn some knobs
- l19: Here are twelve taxi rides, and this is made-up data, just for illustration, not real receipts.
- l20: Each dot is one ride: the further right, the longer the trip, and the higher up, the more it cost.
- l21: If you draw the model's guesses, you get a straight line that gives a fare for every distance.
- l22: The little vertical line from each dot to that line shows how far off the guess was for that ride.
- l23: Let's start by setting the knobs pretty much at random: a base fare of {$0|zero}, and {$1|a dollar} per kilometer.
- l24: The line's way too low, and it guesses too little for all twelve rides.
- l25: Turn the base fare up to {$10|ten dollars}, and the whole line lifts up.
- l26: Now the short rides are pretty close, but the longer the ride, the further off it gets.
- l27: So let's turn the per-kilometer knob, which makes the line steeper.
- l28: At {$3.50|three fifty} a kilometer, we've gone too far, and now it guesses too much for the long rides.
- l29: Turn it back a little, to a base fare around {$10.20|ten twenty} and about {$2.50|two fifty} per kilometer.
- l30: Now the line runs right along the dots, and all those little vertical lines are short.
- l31: Once it's tuned, you can actually use it. So ask it: what would an {8|eight}-kilometer ride cost?
- l32: None of our twelve rides was eight kilometers, but it can still make a guess: about {$30.50|thirty fifty}.

## s4 Where the learning lives
- l33: So step back for a second: what did this machine actually learn?
- l34: Just these two numbers: {$10.20|ten twenty} and {$2.50|two fifty}.
- l35: Everything it picked up from those twelve rides lives in these two readings.
- l36: The machine itself hasn't changed one bit; the only thing that's different is where the knobs are set.
- l37: Copy those two numbers onto a scrap of paper and hand it to a friend, and they've got the exact same model.
- l38: So when people talk about "training a model," what they're really doing is turning knobs.
- l39: And when they say "the model has learned," it means the knobs have been turned to the right positions.

## s5 A hundred billion knobs
- l40: Two knobs are plenty for guessing a taxi fare.
- l41: But if you want a model to write essays or chat with people, you need way, way more knobs.
- l42: In {2020|twenty twenty}, OpenAI released GPT-3, which has {175 billion|a hundred and seventy-five billion} parameters.
- l43: That's a hundred and seventy-five billion knobs.
- l44: How many is that? If you read out one knob setting every second, with no eating and no sleeping, it'd take you over five and a half thousand years.
- l45: Obviously, nobody turned all those knobs by hand; they got their settings from training on huge amounts of text.
- l46: But the idea is exactly the same as with the taxi fare.
- l47: People decide how the machine does its math, and where the knobs end up is learned from examples.
- l48: And when you save a trained model to a file, what's mostly in that file is this long, long list of knob settings.
- l49: So when the news says "a hundred billion parameters," it means the machine has over a hundred billion knobs.

## s6 Wrapping up
- l50: So a model is a machine with knobs, and the parameters are those knobs.
- l51: And learning just means turning the knobs to the right positions.
- l52: But what does "the right positions" actually mean?
- l53: Remember those little vertical lines, some long and some short?
- l54: How do you tell whether one way of setting the knobs is good or bad?
- l55: That's what we'll dig into next time, when we talk about loss functions.
