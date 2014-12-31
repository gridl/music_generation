from __future__ import division
import random
import noise

seed = random.randint(0,1000)
def gen_perlin(length=200, octaves=5):
    noise_array = [0] * length
    max_noise_value = 0.0

    for octave_num in range(octaves):

        cur_step_size = 2 ** octave_num
        # generate the next noise array
        new_noise_values = gen_octave(length=length, step=cur_step_size)

        # add it to our current noise arrays, scaled by the 1/(2 ** (octaves-octave_num))
        # (biggest octave should be scaled at 0.5, smallest at 1/2*octave)
        scale_for_value = 1.0 /  (2 ** (octaves - octave_num))
        max_noise_value += 1.0 * scale_for_value
        for index, value in enumerate(new_noise_values):
            noise_array[index] += value * scale_for_value

    # normalize after everything is done
    noise_array = [ value / max_noise_value for value in noise_array]

    return noise_array

def gen_octave(length, step):
    prev_value = random.random()
    for fill_beginning in range(0, length, step):
        cur_random_val = random.random()
        how_many_to_fill = min(step, length - fill_beginning)
        for how_many_filled in range(how_many_to_fill):
            linear_interpolation_to_new_point = prev_value + (cur_random_val - prev_value) * (how_many_filled / how_many_to_fill)
            octave.append(linear_interpolation_to_new_point)

        prev_value = cur_random_val

    return octave


def gen_perlin_ints(lower, upper, length=200):
    perlin_noise = gen_perlin(length=length)

    int_range = upper - lower

    rounded_perlin_noise = [lower + int(noise_val * int_range) for noise_val in perlin_noise]

    return rounded_perlin_noise

def print_perlin(nums):
    width=10
    for num in nums:
        spacing = int(num * width)
        print "%1.0f%s" % (num, " " * spacing),
        print "|",
        print " " * (width - spacing)


print_perlin(gen_perlin_ints(0,10))
