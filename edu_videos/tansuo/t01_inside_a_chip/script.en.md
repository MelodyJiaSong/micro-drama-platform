# t01 Script (English v2.6, 2026-11-15)

> Spoken English rewrite with the same scenes and line IDs as script.md. This is the targeted-confirmation version after three review rounds. Duration follows the user's quality-first decision.
> v2.5 corrects l34: insulation prevents shorts; alternating routing directions serves layout. The new line awaits independent review; Kimi was quota-blocked.
> v2.6 follows independent Codex review under follow-up 057: gate control voltage, the output signal path, and the magnified atomic view are clarified. See reviews/codex_takeover_r1/ for re-review.

## s1 Where Are We?
- l01: [Kai] ...A city? Like looking down from a plane at night? [pause 1]
- l02: [Kai] ...No way. This is a chip?

## s2 Not One in Sight
- l03: [Kai] A chip this small can hold nineteen billion switches? That's more than two for every person on Earth. But even with my eye practically touching it, I can't see a single one.
- l04: [Lin] It's true. These tiny switches are called transistors. A chip is a tiny slice packed with enormous numbers of them.
- l05: [Kai] Okay... I'll believe half of that for now.

## s3 Who Does the Work When I Tap?
- l06: [Kai] See? One tap, and it lights up. But what's actually happening in there when I tap?
- l07: [Lin] Let's follow that tap inside and find one of the switches it flips.
- l08: [Lin] Each click makes us ten times smaller. We'll shrink to see the switches, then magnify the view to see atoms.
- l09: [Kai] Hang on. How small are we talking? I'm not ready for this—

## s4 Shrinking Down
- l10: [Kai] Whoa, that grain of rice is like a mountain. And that cliff next to it... don't tell me that's a hair.
- l11: [Lin] It's a hair, about 80 to 100 micrometers thick. Follow that blue-white light. That's your tap.

## s5 The Black Case
- l12: [Kai] That black block is the chip, right? It looks more like a chip than anything else on the board.
- l13: [Lin] Close. That's the package, basically its protective case. The actual chip is the thin slice of silicon inside.

## s6 The Solder-Ball Hall
- l14: [Kai] Whoa, it's like an underground parking garage. What are all these shiny balls for, and why are there so many?
- l15: [Lin] Those are solder balls, the doorways between the chip and the motherboard. Power comes in through them, and signals go in and out.
- l16: [Lin] We need so many to supply power, complete circuits, and carry data—not just to connect different parts.

## s7 Opening It Up: It's Face-Down
- l18: [Kai] Oh, it's opening up. So this thin gray slice is the actual chip? Why is it lying face-down?
- l20: [Lin] It's mounted upside down. The side with switches and wiring faces the motherboard, and that's where power and signals go in and out.
- l21: [Kai] Then we need to flip it over.
- l22: [Lin] Okay, let's flip it so we can see. Just to be clear, a real chip doesn't do that.

## s8 A Whole City
- l23: [Kai] It really does look like a city from a plane. Which part is the CPU?
- l24: [Lin] This is the CPU. Let's skip the other names and focus on what these regions share: the switches at the bottom.
- l25: [Lin] But honestly, you couldn't tell these regions apart from up here. We added these colors ourselves.
- l26: [Kai] Wait, you added them?

## s9 Which Area Has the Switches?
- l27: [Kai] So which area has the switches?
- l28: [Lin] All these areas run on transistors. Different components and connections do different jobs.
- l29: [Kai] Then why haven't I seen a single one since we got here?
- l30: [Lin] Because they're at the very bottom, under more than a dozen layers of wiring. Let's head down.

## s10 The Elevator: Highways to Alleyways
- l31: [Kai] All these layers look like highway overpasses. These must be the switches, right?
- l32: [Lin] Nope, these are wires, mostly copper. There are more than a dozen layers.
- l33: [Lin] Up top, long, thick routes carry power and signals like highways. Below, short, narrow connections near the switches form crowded alleys.
- l34: [Lin] Insulating material separates the layers, so crossing wires don't short out. Neighboring layers often run in different directions to make routing easier. Short posts connect the layers where needed.

## s11 Fast Signal, Slow Electrons
- l35: [Kai] Look at that light go. It just zipped around the corner. The electrons must be racing through there, right?
- l36: [Lin] See those little orange dots in the wire? Those are the electrons. They don't travel along with that light.
- l37: [Lin] The electrons jiggle in place and drift slightly. The electric field carries that push forward much faster.
- l39: [Kai] Oh, like a packed subway: everyone shifts a little. But electric fields, not collisions, carry the change, which takes time.

## s12 Why Can't I Take a Picture?
- l40: [Kai] I have to get a picture of this... Huh? Why is it all blurry? Come on, focus!
- l41: [Lin] Your phone isn't the problem. Light itself is too blunt a tool for this.
- l42: [Lin] Visible light spans 400 to 700 nanometers. Here, neighboring wire and transistor features have center-to-center spacing of tens of nanometers, so ordinary optical microscopes struggle to resolve them. More magnification won't help.
- l43: [Lin] Engineers use electron microscopes here, and the raw pictures are gray. We added colors to the chip's materials so we can tell them apart.
- l44: [Kai] ...Whoa, it's all gray. So that's an electron-microscope image. Like an old photograph.

## s13 The Very Bottom
- l45: [Kai] Finally, the bottom. Hey, people always talk about three nanometers. Which part is three nanometers, these walls or the gaps between them?
- l46: [Lin] In one advanced process, these walls are called gates. Their centers are about 50 nanometers apart, so 1,600 to 2,000 gates could fit side by side across one hair.
- l47: [Lin] So don't expect to measure three nanometers with a ruler here. It's a process name, like a car model. It doesn't match any single edge.

## s14 Where's the Handle?
- l49: [Kai] This is a switch? Shouldn't a switch have some kind of handle? But nothing's moving. How does it turn on and off?
- l50: [Lin] Picture an advanced nanosheet switch. Three or four super-thin silicon sheets, each about six nanometers thick, connect the two ends. The gate wraps around every sheet.
- l51: [Lin] That handle you want? Some early computers did have something like that. They used relays. Apply power, and an electromagnet pulls a piece of iron over. Click—the contacts touch.
- l52: [Lin] But here, not a single part moves.
- l53: [Kai] No mechanical parts move at all... Does it still count as a switch?

## s15 First, Why Is It Off?
- l54: [Lin] This N-type transistor is normally off. Why?
- l55: [Kai] But with no gate voltage, doesn't silicon still have electrons?
- l56: [Lin] It does, but they haven't formed a channel connecting the two ends. So right now, it's off.
- l57: [Kai] So the silicon stays. It's the path that's missing, not the material?
- l58: [Lin] Right. We're not building a physical road. The silicon stays in place. More electrons make it conductive. Watch the gate do it.

## s16 Voltage On, Current Flows. Voltage Off, It Stops.
- l59: [Lin] A very thin insulator separates the gate from the silicon. The field acts through it, but any gate leakage into the silicon is normally tiny.
- l60: [Lin] Now let's put a voltage on the gate. See? The electric field reaches through the insulator and pulls electrons in the silicon toward the insulating layer.
- l61: [Lin] More and more electrons gather there and form a continuous channel. The two ends are connected.
- l62: [Lin] Now take the voltage away. The electrons spread out, the channel disappears, and it's off again. [pause 1]
- l63: [Lin] The whole time, not one mechanical part moved. What changed was the electric field and where the electrons were.
- l64: [Kai] Wait, there's an insulator in the way. The gate can't even touch those electrons, so how can it pull them over?
- l65: [Lin] You know how a magnet can move iron filings even through a tabletop? It's pulling without touching them. Something similar is happening here, except this is an electric field, not a magnetic one.
- l66: [Kai] ...That's it? I thought there'd be some tiny hidden mechanism in there.
- l67: [Lin] That's it. Enough positive voltage turns it on. Take it away, and it turns off.

## s17 Why Wrap It So Completely?
- l68: [Kai] It's wrapped up tightly on all four sides. Why go that far? Wouldn't covering one side be enough?
- l69: [Lin] The more the gate wraps, the better it usually controls the channel. Less current leaks when it's off, but off doesn't mean zero current. A tiny amount can get through.
- l70: [Lin] That's why the design evolved from flat layers to upright fin channels, and now to gates wrapping all four sides.

## s18 Ones and Zeros
- l71: [Kai] Here it comes, that's my tap! ...But what does one switch turning on and off have to do with the photos and messages on my phone?
- l72: [Lin] In a chip, high and low voltages often represent ones and zeros. Switches turn on and off to create and pass along these signals.
- l73: [Lin] Two different types of switches can work together as an inverter. A one becomes a zero, and a zero becomes a one. An inverter can't store photos by itself. Different circuits work together to make decisions, store photos, and play videos.
- l74: [Lin] Your tap reaches the gate: the channel conducts, changing the output voltage. A wire carries that change to the next stage.
- l75: [Kai] So my tap really did make it all the way here... Found you.

## s19 Counting Atoms
- l76: [Kai] One, two, three, four... five... [pause 1]
- l77: [Lin] In this six-nanometer example, each sheet is only forty-something atomic layers thick. Engineers really can make silicon sheets this thin.
- l78: [Kai] ...Ten or twenty billion switches, made and wired together on a silicon slice.

## s20 How Much Smaller Are We?
- l79: [Lin] Guess how much smaller we are now.
- l80: [Kai] Hmm... Ten thousand times? The dial only clicked a few times.
- l81: [Lin] Seven clicks and a bit, each making us ten times smaller. We're about 100 nanometers tall now, seventeen million times smaller than before.
- l82: [Kai] Seventeen million?...

## s21 Now Flip It Around
- l83: [Kai] What if we enlarged the chip seventeen million times too? Would each switch take up as much space as we do?
- l84: [Lin] Yes. Each switch would take up just over a square meter on average. The chip would cover about twice Beijing's area. That's how a fingernail-sized slice holds ten or twenty billion switches.
- l85: [Kai] Two Beijings... and I carry that around in my pocket every day?

## s22 Heading Back
- l86: [Lin] Hold on. We're heading home.
- l87: [Kai] Woohoo, homeward bound!

## s23 One Last Thought and What's Next
- l88: [Kai] {Let me check. |}Below, ten or twenty billion switches have no moving parts. Electric fields control whether they conduct. Above, over a dozen wiring layers connect them like a city. It's all face-down inside that black package. Right?
- l89: [Lin] Exactly. You've got it.
- l90: [Kai] ...But wait. If all they can do is turn on and off, how do they figure out that one plus one is two?
- l91: [Lin] Ah, that's for next time. We'll head back in and find out.
