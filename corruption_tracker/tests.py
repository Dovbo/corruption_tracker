from corruption_tracker.test_runner import perfomance_test


def run_home():
    perfomance_test('/')

def run_kha_distritc():
    perfomance_test('/api/polygon/fit_bounds/3/35.92289,49.88977,36.58207,50.08909/')

def kha_houses():
    perfomance_test('/api/polygon/fit_bounds/4/36.08374,49.96337,36.41333,50.03575/')




# run_home()
# run_kha_distritc()
kha_houses()