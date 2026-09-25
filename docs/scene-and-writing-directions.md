# Scene and writing directions

## Review of Copilot's proposal

Reviewed `bigcub-add-new-landscape-scene` at `3114ef8`, including a browser preview.

The observatory and forest lookout are useful concepts. Their rendering needs the same lighting, depth, and silhouette work as the current meadow and coast. The forest's triangular trees are too repetitive, and the observatory's dome and telescope need a more convincing construction. The desert foreground rendered black in the reviewed preview. Both scenes retain the opaque moon cutout that we fixed in the main artwork.

The permanent article shelf covers some of the studio and foreground. David confirmed that this is the preferred hierarchy: the articles are the purpose of the site and should be immediately visible. The separate archive is a useful eventual destination, but the sample entries are only summaries, not working articles. Its theme also does not initialise from the saved preference.

## Scene shortlist

These are illustration concepts, not claims about specific locations.

| Priority | Scene | Composition and light | Restrained movement |
| --- | --- | --- | --- |
| 1 | Mountain tarn | Angular peaks, a still lake, a small stone bothy; warm summit light by day, indigo reflections at night | Ripples and drifting valley mist |
| 2 | Woodland lookout | Irregular pine silhouettes framing a small timber tower; shafts of amber light, warm windows at night | Branch tips and an occasional owl |
| 3 | Desert observatory | Sweeping dunes with clear lit and shaded faces; a small dome against a large rose-to-violet sky | Slow dome movement and rare meteors |
| 4 | Canal at dusk | A narrowboat, brick bridge, towpath and reflected windows; a more urban companion to the meadow | Reflections and a slow passing boat |
| 5 | Winter cabin | Snow banks, bare branches and a warm cabin; pale daylight and blue moonlit snow | A few snowflakes and chimney smoke |

Start with the mountain tarn for the biggest compositional change. The woodland lookout is the strongest concept to retain from Copilot. Give each scene one focal structure and one occasional animated event. Compose the phone crop deliberately. The cycling button stays: David decided against a named scene picker, even with more scenes. The left and right arrow keys also step through the scenes.

## Writing access

Revised after David's feedback: articles are the primary purpose of the site. The landscape supports them. Use Copilot's always-visible shelf, with a featured article, two supporting titles, and a View all articles link. Do not hide the articles behind an initial click.

The revised prototype retains the current artwork and uses a glass panel with stronger text contrast in both themes. Mobile keeps all three titles visible and allows page scrolling on short screens. Titles link to a clearly labelled preview archive, without invented reading times. All article text remains illustrative.

The prior hidden Writing button and modal have been removed. No new scenes have been implemented.

The shelf now has a more transparent background and lighter blur. A small Hide articles / Show articles toggle lets visitors enjoy the scene. Articles are visible on every fresh page load; the hidden choice is not saved.

Implemented Blea Tarn as a stylised mountain scene with an imagined bothy, reflected peaks, ducks, birds, water rings and layered pointer parallax. The icon button cycles Meadow → Coast → Blea Tarn and saves the choice in localStorage. Coordinates are rounded to match existing scenes, using the Blea Tarn area in https://longvalleybooks.com/wp-content/uploads/2017/11/GPSLakeDistrict.pdf as reference.

Implemented the Kielder woodland lookout, with pines, mist, owl flight, pollen, swaying ferns and pointer parallax. The tower is illustrative. Coordinates rounded from https://www.britishplacenames.uk/kielder-forest-northumberland-ny665905 .

Forest is now the default for new visitors and invalid saved choices. Valid scene preferences remain respected. The nocturnal owl has a cream facial disc, barred feathers and a slower glide-and-wingbeat animation; the robin remains daytime-only.

Implemented the desert observatory at Merthyr Mawr, whose dunes are the UK's best-known desert stand-in. The scene has sculpted dunes with lit and shaded faces under a rose-to-violet sky, and an imagined domed observatory. The dome's shutter and telescope turn slowly, sand lifts from the crests and marram grass sways. At night the shutter shows a red working light, the door is lit, a faint Milky Way appears and three meteors cross at long, staggered intervals. On phones the observatory dune moves into the centre crop and rises clear of the notes shelf. The cycle is now Meadow → Coast → Blea Tarn → Kielder Forest → Merthyr Mawr. Coordinates rounded from https://en.wikipedia.org/wiki/Merthyr_Mawr_Sand_Dunes (51.48° N, 3.64° W).

Refined the desert so it holds its own in the cycle. The dunes now have curved slip faces instead of flat, vertical-edged shading. A strip of the Bristol Channel shows between the far dunes, with sun or moon glints and a low far shore. Marram tufts and a line of sand fencing give the dunes scale, and long soft clouds cross the sky. A kestrel hovers over the dunes by day; the meteors stay night-only.

Implemented the canal at dusk in Manchester, drawn from Castlefield, as an urban companion to the meadow. Brick warehouses with arched windows and loading doors stand along the quay, a humped brick bridge carries the towpath over the mouth of a canal arm, and a green narrowboat is moored beside it, smoke rising from its chimney. A railway viaduct runs behind with Beetham Tower beyond, and a tram crosses the viaduct and slips behind a warehouse. The water carries soft, shimmering reflections, and a blue narrowboat slowly passes. At night the warehouse windows, the lamp on the towpath, the boats and the tram light up, and the low sun becomes a moon. The focus sits on the left, clear of the notes; on phones the canal lifts and shifts so the bridge and moored boat sit above the notes. The cycle is now Meadow → Coast → Blea Tarn → Kielder Forest → Merthyr Mawr → Manchester canal. Coordinates rounded from https://en.wikipedia.org/wiki/Castlefield (53.475° N, 2.255° W).

The meadow and its studio are now located at Eagley, near Bolton, rather than Manchester. Coordinates rounded from https://en.wikipedia.org/wiki/Eagley (53.617° N, 2.432° W).
