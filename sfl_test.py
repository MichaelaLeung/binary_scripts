import numpy as np

def sfl_test(pair, i):
    weights_in =
    in_1 = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/g2v_surf.pdat'
    g_data = np.genfromtxt(in_1)
    if pair == 'GG' 
        data_2 = g_data
        weights_in = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GGTweights.csv'
        weights = np.genfromtxt(weights_in)
        weights = weights[0,:]
    else:
        in_2 = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/adleo_photo.pdat'
        data_2 = np.genfromtxt(in_1)
        weights_in = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GMTweights.csv'
        weights = np.genfromtxt(weights_in)
        weights = weights[0,:]
    g_final = g_data[i,2]
    data_2 = data_2[i,2]

    final = g_final * weights[0] + data_2 * weights[1]
    return final 

    


if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="phase_T",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "72:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        sfl_test('GG',10)
     else:
        phase_temp()
