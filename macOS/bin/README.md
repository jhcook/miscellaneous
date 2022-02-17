# Introduction

Here are things you may use on the command line in on macOS. 

## Games

### Wordle

It took social media by storm, and then NY Times bought it!

This is my training wheel version for mere mortals.

```
 ./wordle.py
Enter 1st word: reset
⬛️🟩⬛️🟨⬛️
Suggestions: aevia, beach, beady, beaky, beala, beamy, beano, beany, beaux, bebay, bebog, bebop, becap, bedad, beday, bedim, bedin, bedip, bedog, bedub, bedye, beech, beefy, beeve, befan, befog, befop, begad, begay, begin, begob, begum, begun, behap, beice, beige, being, bejan, bejig, bekah, bekko, belah, belam, belay, belch, belga, belie, belle, belly, below, belve, bemad, beman, bemix, bemud, benab, bench, benda, bendy, benjy, benne, benny, benzo, beode, bepaw, bepun, bevue, bewig, bezzi, bezzo, cebid, cebil, ceibo, ceile, cella, cello, cequi, deave, debby, decad, decal, decan, decap, decay, decil, decke, decoy, decyl, deedy, defog, degum, deice, deify, deign, deink, dekko, dekle, delay, delve, demal, demob, demon, denda, denim, depoh, deuce, devil, devow, dewan, dewax, feaze, fecal, feedy, feeze, feign, felid, felly, felon, femic, fence, fendy, fenny, feoff, fezzy, gecko, gelid, gelly, gemma, gemmy, gemul, genal, genic, genie, genii, genin, genip, genom, genua, geode, geoid, geyan, heady, heald, heapy, heave, heavy, hedge, hedgy, heedy, heeze, heezy, heiau, heigh, helio, helix, hello, helly, heloe, helve, hemad, hemal, hemic, hemin, hemol, hempy, henad, hence, henna, henny, heuau, heugh, hexad, hexyl, jehup, jelab, jelly, jemmy, jenna, jenny, keach, keawe, kebab, kecky, kedge, keech, keena, keeve, kella, kelly, kelpy, kempy, kenaf, kench, kenno, leach, leady, leafy, leaky, leave, leavy, leban, ledge, ledgy, ledol, leech, leeky, legal, leggy, legoa, legua, lehua, lekha, leman, lemma, lemon, lenad, lench, leuch, leuco, leuma, levin, lexia, mealy, mecon, medal, media, medic, medio, meece, meile, melam, melch, melic, meloe, melon, mezzo, nebby, neddy, needy, neeld, neele, neeze, neffy, neigh, neoza, neuma, neume, nevoy, newly, nexal, nexum, oenin, peace, peach, peage, peaky, peavy, pecan, pecky, pedal, pedum, peele, peeoy, peepy, peeve, peggy, peine, pekan, pekin, pekoe, pelon, penal, pence, penda, pengo, penna, penni, penny, peony, peppy, peuhl, vealy, veily, veiny, velal, velic, velum, venal, venie, venin, venom, venue, veuve, vexil, weaky, weald, weave, webby, wedge, wedgy, weeda, weedy, weeny, weepy, weeze, weigh, wekau, welly, wench, wende, wenny, xenia, xenon, xenyl, yeuky, yezzy, zebub, zemmi, zemni
Enter 2nd word: heady
⬛️🟩⬛️⬛️🟩
Suggestions: beefy, belly, benjy, benny, felly, fenny, fezzy, gelly, gemmy, jelly, jemmy, jenny, kecky, kelly, kelpy, kempy, leeky, leggy, nebby, neffy, nevoy, newly, pecky, peeoy, peepy, peggy, penny, peony, peppy, veily, veiny, webby, weeny, weepy, welly, wenny, yeuky, yezzy
Enter 3rd word: newly
🟨🟩⬛️⬛️🟩
Suggestions: benjy, benny, fenny, jenny, nebby, neffy, nevoy, penny, peony, veiny
Enter 4th word: jenny
Good job!
```

## Wordle Solver

This tool uses a dictionary of words with hints provided and suggests possible
answers matching the hints. In the example below, the `!` character is used to
mark the character as yellow, i.e., used in the word but not that position.
Green characters are marked as just the letter for that position and duds are
known black out or letters known not to be used in the word. The following is a
real-world example with the answer being _caulk_ in Wordle 242. The dictionary
can be found on [Github](https://raw.githubusercontent.com/dwyl/english-words/master/words.txt). 

Potential candidates are sorted by [letter frequency](https://artofproblemsolving.com/news/articles/the-math-of-winning-wordle).

A good list of [words on AoPS Online](https://artofproblemsolving.com/texer/vxeinejf) is a great source.

Below, the first word was _lunch_. The hints provided the following suggestions
and the second word choice was _oculi_. The hints provided fewer suggestions
with _caulk_ selected as the correct final choice.

```
 ./wsolver.py
1st known letter: !l
2nd known letter: !u
3rd known letter:
4th known letter: !c
5th known letter:
Known duds: nh
Suggestions: cauld, cauli, caulk, cauls, claut, cleuk, clour, clout, clubs, clued, clues, cluff, clump, could, cruel, crull, oculi, picul, pocul, scaul, sculk, scull, sculp, scult, ticul, ulcer, ulcus, ulmic

 ./wsolver.py
1st known letter:
2nd known letter: !c
3rd known letter: u
4th known letter: l
5th known letter:
Known duds: oi
Suggestions: cauld, caulk, cauls, crull
```

Multiple round of hints can be provided in one go. For example, the above hints
are combined below. Note that known letters (green) override yellow or unknown
position letters.

```
 ./wsolver.py
1st known letter: !l
2nd known letter: !uc
3rd known letter: u
4th known letter: l
5th known letter:
Known duds: nhoi
Suggestions: cauld, caulk, cauls, crull
```
