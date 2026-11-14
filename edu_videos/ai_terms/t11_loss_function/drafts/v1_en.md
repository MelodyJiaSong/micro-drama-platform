## s0 Cold open
- l01: Last time, we said a model is just a machine with knobs, and learning means turning those knobs to the right spot.
- l02: But what does "right" even mean?
- l03: And how is the machine supposed to know that this turn was any better than the last one?
- l04: The trick is to give its mistakes a score.
- l05: That score is called the loss, and the rule for working it out is called the loss function, which is what today is all about.

## s2 What a loss function is
- l06: Every time the model makes a guess, it's going to be a bit off from the real answer.
- l07: How far off it is, that's called the error.
- l08: Roll a whole pile of those errors up into one number, and that number is the loss: a score for how wrong it is this time.
- l09: And it works the opposite way from a test score: lower is better, and zero is perfect, meaning not wrong at all.
- l10: It's kind of like golf, where fewer strokes is better.
- l11: Once it has that score, the machine can check its own work.
- l12: Turn a knob a little: if the score goes down, that was the right turn, and if it goes up, turn it back.
- l13: So training, put simply, is just turning the knobs over and over to push that score down.

## s3 A little experiment
- l14: Let's go back to those twelve taxi rides from last time, with distance along the bottom and fare up the side.
- l15: And just so you know, this data is made up for illustration.
- l16: The model is still that same straight line: the fare is a starting fare, plus so much per kilometer times the distance.
- l17: That gives us two knobs: the starting fare, and the price per kilometer.
- l18: First try: a {$5|five-dollar} starting fare and {$2|two dollars} per kilometer.
- l19: This whole line sits too low, underneath the points.
- l20: Take one ride: the {5|five}-kilometer trip actually cost {$23|twenty-three dollars}, but the model guessed {$15|fifteen}, so it's off by {$8|eight dollars}.
- l21: That gap is the error.
- l22: Now square it: eight times eight is {64|sixty-four}.
- l23: Do that for all twelve rides, error then square, take the average, and this setting scores {78|seventy-eight}.
- l24: Second try: a {$4|four-dollar} starting fare and {$3.50|three fifty} per kilometer.
- l25: This line is way too steep: it guesses too low on the short rides and too high on the long ones.
- l26: Now, if we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel each other out.
- l27: The average comes out to only about {−$0.30|minus thirty cents}, which makes it look like it's barely wrong at all.
- l28: That's exactly why we square: once everything's squared, it's all positive, so nothing can cancel out.
- l29: And the bigger the miss, the harsher the penalty: off by two costs you four, but off by eight costs you {64|sixty-four}.
- l30: Square, then average, and this setting scores {13.4|thirteen point four}.
- l31: This way of scoring is called mean squared error, and it's the most common loss function, though not the only one.
- l32: Third try: a {$10|ten-dollar} starting fare and {$2.50|two fifty} per kilometer.
- l33: This line hugs the points pretty closely, the squares are all tiny, and it scores {2.19|two point one nine}.
- l34: Put them side by side, {78|seventy-eight}, {13.4|thirteen point four}, {2.19|two point one nine}, and the third has the lowest score, so it's the best setting.
- l35: But that's only three tries.
- l36: If we scored every possible way of setting the two knobs, we could draw the scores as a kind of landscape map.
- l37: Starting fare runs along the bottom, price per kilometer runs up the side, and the darker the color, the higher the score.
- l38: Each of our three tries is just one point on this map.
- l39: The first is way up high, the second is halfway down the slope, and the third is nearly at the bottom of the valley.
- l40: The lowest point on the whole map is a starting fare of about {$10.20|ten twenty}, with about {$2.54|two fifty-four} per kilometer.
- l41: It scores {1.97|one point nine seven}, and that's the best possible setting for this data.
- l42: And the whole job of training is to find that lowest point on the map.

## s4 The model only cares about the score
- l43: Here's something easy to miss: even the lowest point isn't zero.
- l44: Real fares bounce around randomly with traffic and detours, so no straight line could nail every single ride.
- l45: So training isn't chasing a perfect zero; it's chasing as low as it can get.
- l46: And here's the other thing: the model has no idea what a taxi is.
- l47: All it cares about is the score, and however you score it, that's the direction it learns in.
- l48: Because we squared the errors, for example, it's terrified of big mistakes.
- l49: It would rather be a little off on every ride than way off on just one.
- l50: So when you pick a loss function, what you're really doing is telling the model what "good" means.

## s5 How big models get scored
- l51: Big language models like ChatGPT get a score during training too; it's just scoring something different.
- l52: Their job is to guess the next word, like "Twinkle, twinkle, little…" star.
- l53: The score looks at how confident the model was about the word that actually comes next.
- l54: The more confident it was, the smaller the penalty, and the less confident, the bigger the penalty.
- l55: Give the right word {90%|ninety percent} confidence, and the penalty is tiny, about {0.11|zero point one one}.
- l56: Give it only {10%|ten percent}, and the penalty is way bigger, about {2.3|two point three}.
- l57: This way of scoring is called cross-entropy, and honestly, the name is all you need for now.
- l58: Here's a real example: in {2023|twenty twenty-three}, Meta trained a large language model called Llama 2.
- l59: They plotted this score as a curve, and it just kept going down.
- l60: After the model had read {2 trillion|two trillion} tokens of data, which are roughly words or pieces of words, the score was still falling.
- l61: There was no sign yet of it hitting a floor.
- l62: Whether it's a hundred billion knobs or just two, the job is the same: push that score down.

## s6 Wrap-up
- l63: So, a loss function is a score for how wrong the model is, and lower is better.
- l64: And training is just pushing that score down.
- l65: But once there are tons of knobs, that map gets so huge you can't even see the edges.
- l66: So how do you know which way to turn, to work your way down, step by step, to the lowest point?
- l67: That's gradient descent, and that's where we're headed next time.
