PF2E Threat Levels:     XP Budget per Character:
Trivial                 10
Low                     15
Moderate                20
Severe                  30
Extreme                 40

Total XP Budget = Party Size * Threat Level(user input)
Party Level = Average level of party members

Party Level Cap = 14?
Party Size Cap = 8?

Encounter Size Cap = TDB

XP per Monster = Monster level compared to Party Level
Party level - 4 = 10xp
Party level - 3 = 15xp
Party level - 2 = 20xp
Party level - 1 = 30xp
Party level     = 40xp
Party level + 1 = 60xp
Party level + 2 = 80xp
Party level + 3 = 120xp
Party level + 4 = 160xp

Query Logic:

Get Total XP Budget
Filter db based on Party Level (Exclude monsters not within above xp range)
 {
    Pick monster at random
    Compare Monster Level to Party Level to determine xp value
    Compare Monster XP Value to Remaining XP Budget
        If Monster XP Value <= Remaing XP Budget:
            Subtract Monster XP Value from Remaining XP Budget
            Add Monster to Encounter
 }
 Repeat bracketed steps until Remaining XP Budget is 0
 Output Encounter