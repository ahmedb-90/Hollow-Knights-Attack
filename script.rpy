# HOLLOW CROWN - Wick the Warden fights his way to the tyrant king.

# ---------- characters (who is talking) ----------
define wick = Character("Wick", color="#8fe9f2")
define cask = Character("Cask", color="#e2c36a")
define shade = Character("The Shade", color="#b79aef")
define king = Character("King Marrowgast", color="#b79aef")

# ---------- sprites (the pictures) ----------
# The PNG files live in the game/images folder.
image bg gate = "bg gate.png"
image bg archive = "bg archive.png"
image bg throne = "bg throne.png"

image wick idle = "wick idle.png"
image wick attack = "wick attack.png"
image wick hurt = "wick hurt.png"

image cask idle = "cask idle.png"
image cask attack = "cask attack.png"
image cask hurt = "cask hurt.png"

image shade idle = "shade idle.png"
image shade attack = "shade attack.png"
image shade hurt = "shade hurt.png"

image king idle = "king idle.png"
image king attack = "king attack.png"
image king hurt = "king hurt.png"

# ---------- positions and animations ----------
transform left_spot:
    xalign 0.15 yalign 1.0

transform right_spot:
    xalign 0.85 yalign 1.0

transform bob:            # breathing
    ease 0.8 yoffset -10
    ease 0.8 yoffset 0
    repeat

transform shake:          # getting hit
    linear 0.05 xoffset -25
    linear 0.05 xoffset 25
    linear 0.05 xoffset 0

transform hero_lunge:     # Wick jumps forward
    linear 0.12 xoffset 300
    linear 0.2 xoffset 0

transform foe_lunge:      # enemy jumps forward
    linear 0.12 xoffset -300
    linear 0.2 xoffset 0

# ---------- variables ----------
default hp = 5
default max_hp = 5
default foe = "cask"      # which enemy sprite to use
default foe_hp = 3
default foe_max = 3
default crown_dmg = 1
default route = ""
default attack = 0
default attack_text = ""
default hit = False

screen hud():
    text "Wick HP: [hp]" xpos 40 ypos 30 size 36
    text "Enemy HP: [foe_hp]" xalign 0.96 ypos 30 size 36

# =========== STORY ===========
label start:

    scene bg gate with fade
    show wick idle at left_spot, bob
    wick "King Marrowgast! Open the gate!"

    show cask idle as enemy at right_spot, bob
    cask "The king answers to nobody. Leave, Warden."
    wick "No."

    menu:
        "Which way?"
        "Smash through the gate":
            jump gate_road
        "Sneak through the tunnel":
            jump tunnel_road

label gate_road:
    $ route = "gate"
    cask "Then come and get it."
    $ foe = "cask"
    $ foe_hp = 3
    $ foe_max = 3
    call fight
    cask "...Fine. Take my armor."
    $ max_hp = 7
    "ARMOR! Wick now has 7 HP."
    jump throne

label tunnel_road:
    $ route = "tunnel"
    scene bg archive with fade
    show wick idle at left_spot, bob
    show shade idle as enemy at right_spot, bob
    shade "...give... me... your light..."
    wick "Not a chance."
    $ foe = "shade"
    $ foe_hp = 4
    $ foe_max = 4
    call fight
    "The Shade drops a silver needle. Crown strikes now do double damage!"
    $ crown_dmg = 2
    jump throne

label throne:
    scene bg throne with fade
    show wick idle at left_spot, bob
    show king idle as enemy at right_spot, bob

    if route == "gate":
        king "You broke my gate? Expensive."
    else:
        king "You crawled through my tunnels? Cute."

    wick "Four thousand stolen lanterns. You're done, Marrowgast."
    king "Then make me."

    $ foe = "king"
    $ foe_hp = 8
    $ foe_max = 8
    call fight

    show king hurt as enemy at right_spot
    king "Impossible..."
    wick "Guilty."
    with Fade(0.1, 0.0, 0.5, color="#ffffff")
    "The crown cracks in two. Every lantern in the city lights up."

    scene black with fade
    centered "THE END"
    return

# =========== THE FIGHT (used for every enemy) ===========
label fight:
    $ hp = max_hp
    show screen hud

label fight_round:
    if foe_hp <= 0:
        hide screen hud
        return

    if hp <= 0:
        "You fall... and get back up!"
        $ hp = max_hp
        $ foe_hp = foe_max

    # 1 = low, 2 = high, 3 = the crown glows (king only)
    if foe == "king":
        $ attack = renpy.random.randint(1, 3)
    else:
        $ attack = renpy.random.randint(1, 2)

    if attack == 1:
        $ attack_text = "LOW attack!"
    elif attack == 2:
        $ attack_text = "HIGH attack!"
    else:
        $ attack_text = "The crown GLOWS!"

    menu:
        "[attack_text]"
        "Jump":
            $ hit = attack == 1
        "Duck":
            $ hit = attack == 2
        "Strike the crown" if foe == "king":
            $ hit = attack == 3

    if hit:
        show wick attack at left_spot, hero_lunge
        show expression (foe + " hurt") as enemy at right_spot, shake
        if attack == 3:
            $ foe_hp -= crown_dmg
        else:
            $ foe_hp -= 1
        "You hit back!"
    else:
        show expression (foe + " attack") as enemy at right_spot, foe_lunge
        show wick hurt at left_spot, shake
        $ hp -= 1
        "You get hit!"

    show wick idle at left_spot, bob
    show expression (foe + " idle") as enemy at right_spot, bob
    jump fight_round
