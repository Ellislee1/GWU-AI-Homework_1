def test1(env):
    env.fill(-2,1)
    print(env)

    env.fill(1,-1)
    print(env)

    env.fill(-2,1)
    print(env)

    env.fill(1,-1)
    print(env)

    env.fill(-1,0)
    print(env)

    env.fill(-1,1)
    print(env)

    print(env.get_state())

def test2(env):
    # Cycle 1
    env.fill(-2,1)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)

    # Cycle 2
    env.fill(-2,1)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)

    # Cycle 3
    env.fill(-2,1)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)

    # Cycle 2
    env.fill(-2,1)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)

    env.fill(0,-2)
    print(env)

    env.fill(1,0)
    print(env)


    