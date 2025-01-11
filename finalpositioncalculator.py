#This is a code that calculates the final position based on the initial position and a initial velocity iteratively of a block-spring system
#The block is under the influence of both the spring force and the graviational force
#The higher the t, value given by the user, better the estimate


import numpy as np

def net_force(initial_pos, relaxed_length, mass_block, spring_stiffness):
    s_vector = initial_pos - np.array([0, relaxed_length, 0])
    net = -spring_stiffness * s_vector + mass_block * np.array([0, -9.8, 0])
    return net

def final_momentum(initial_v, net_force, t, mass_block):
    initial_momentum = mass_block * initial_v
    final = initial_momentum + net_force * t
    return final

def final_position(initial_pos, initial_v, t, mass_block, relaxed_length, spring_stiffness):
    average_v = final_momentum(initial_v, net_force(initial_pos, relaxed_length, mass_block, spring_stiffness), t, mass_block) / mass_block
    final = initial_pos + np.round(average_v, 3) * t
    return final

def user_input():
    spring_stiffness = float(input("Spring stiffness (N/m): "))
    relaxed_length = float(input("Relaxed length (m): "))
    mass_block = float(input("Mass of the block (kg): "))
    initial_velocity = input("Initial velocity (m/s) in format a,b,c: ")
    a, b, c = map(float, initial_velocity.split(","))
    initial_v = np.round(np.array([a, b, c]), 3)
    
    initial_position = input("Initial position from the base of the spring (m) in format a,b,c: ")
    a, b, c = map(float, initial_position.split(","))
    initial_pos = np.round(np.array([a, b, c]), 3)
    
    t = float(input("Time step: "))
    t_final = float(input("When do you want the position of the ball at: "))
    
    return spring_stiffness, relaxed_length, mass_block, initial_v, initial_pos, t, t_final

def main():
    spring_stiffness, relaxed_length, mass_block, initial_v, initial_pos, t, t_final = user_input()
    
    t_loop = t
    while t_loop <= t_final:

        f_net_force = net_force(initial_pos, relaxed_length, mass_block, spring_stiffness)
        f_momentum = final_momentum(initial_v, f_net_force, t, mass_block)
        f_position = final_position(initial_pos, initial_v, t, mass_block, relaxed_length, spring_stiffness)
        

        initial_v = f_momentum / mass_block
        initial_pos = f_position
        
        t_loop += t

    print("Final Momentum:", f_momentum)
    print("Final Position:", f_position)

if __name__ == "__main__":
    main()
