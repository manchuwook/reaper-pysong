import pydash
import random
import song_library


def generateStructure():
    preintro = song_library.SongPart(
        name='Pre-intro', bars=random.choice(
            [4, 8]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.PRE_INTRO,
        variation=None
    )
    intro = song_library.SongPart(
        name='Intro', bars=random.choice(
            [4, 8, 16]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.INTRO,
        variation=None
    )
    outro = song_library.SongPart(
        name='Outro', bars=random.choice(
            [4, 8, 16]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.OUTRO,
        variation=None
    )
    preoutro = song_library.SongPart(
        name='Pre-outro', bars=random.choice(
            [4, 8]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.PRE_OUTRO,
        variation=None
    )
    preverse = song_library.SongPart(
        name='Pre-verse', bars=4, color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.PRE_VERSE,
        variation=None
    )
    verse = song_library.SongPart(
        name='Verse', bars=random.choice(
            [4, 8, 16]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.VERSE,
        variation=None
    )
    prechorus = song_library.SongPart(
        name='Pre-chorus', bars=4, color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.PRE_CHORUS,
        variation=None
    )
    chorus = song_library.SongPart(
        name='Chorus', bars=random.choice(
            [4, 8, 16]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.CHORUS,
        variation=None
    )
    bridge = song_library.SongPart(
        name='Bridge', bars=8, color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.BRIDGE,
        variation=None
    )
    breakdown = song_library.SongPart(
        name='Breakdown', bars=random.choice(
            [4, 8]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.BREAKDOWN,
        variation=None
    )
    instrumental = song_library.SongPart(
        name='Instrumental', bars=random.choice(
            [4, 8]
        ), color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.INSTRUMENTAL,
        variation=None
    )
    drop = song_library.SongPart(
        name='Drop', bars=4, color='red', index=None,
        max=None, min=None,
        type=song_library.TypeEnum.DROP,
        variation=None
    )

    v_accum = 0
    c_accum = 0

    structures = pydash.chain([]).push(
        random.choice([
            [preintro, intro],
            intro, None
        ])
    ).push(
        random.choices(
            population=[
                [preverse, verse],
                verse,
                [prechorus, chorus],
                chorus,
                None
            ],
            weights=[1, 2, 1, 2, 1], k=8
        )
    ).push(
        random.choices(
            population=[
                [breakdown, bridge],
                [drop, breakdown],
                [breakdown, instrumental],
                breakdown,
                bridge,
                instrumental,
                None
            ],
            weights=[1, 2, 2, 2, 2, 1, 1], k=1
        )
    ).push(
        random.choices(
            population=[
                chorus,
                verse,
                None
            ],
            weights=[2, 2, 1], k=1
        )
    ).push(
        random.choice([[preoutro, outro], outro, None])
    ).flatten_deep().compact().value()

    part: song_library.SongPart
    # Naming of the parts (Verse 1, Chorus 1, Verse 2, Chorus 2, etc.)
    for idx, part in enumerate(structures):
        # Create a copy of the part to swap out base classes
        p: song_library.SongPart = song_library.SongPart(
            name=part.name, bars=part.bars, color=part.color, index=part.index,
            max=part.max, min=part.min, type=part.type, variation=part.variation
        )
        if part.type == song_library.TypeEnum.CHORUS:
            c_accum = c_accum + 1
            p.name = part.name + ' ' + str(c_accum)
        if part.type == song_library.TypeEnum.VERSE:
            v_accum = v_accum + 1
            p.name = part.name + ' ' + str(v_accum)
        structures[idx] = p

    pydash.for_each(structures, lambda x: print(
        str(x.type.value) + ': ' + str(x.name)
    ))
    song = song_library.SongLibraryElement('Generated Song', structures)
    return song


generateStructure()
