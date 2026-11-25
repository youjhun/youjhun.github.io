"""GRABMyo F1 replay sources. Python 3 + numpy; generated data: CC BY 4.0.

Jiang, Pradhan & He, GRABMyo v1.1.0 (2024), doi:10.13026/89dm-f662.
No extra filtering, centering, normalization or hardware-gain division.
Only the two pinned format-16 records below are supported.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import urllib.request
import numpy as np

BASE = 'https://physionet.org/files/grabmyo/1.1.0/Session1/session1_participant1/'
RECORDS = {
    'rest': ('session1_participant1_gesture17_trial1',
             'aed261955a348275e791a8a24bbbdb272f5aa7936615e6fe938912ef75a935bf',
             '6f954b66c34c1d5b0de348879bb05c79f49c5e2e91d0f6e7e3e7624811353a93'),
    'hand_close': ('session1_participant1_gesture16_trial1',
                   '414b699ae5858e89b636260ab022016cb89010504301d74850575daab53e5ec2',
                   'cb419b513c756966bc803c729ca68743f3188571d9efda8cfe00a86b92149861'),
}
COMPOSITE = '''.SUBCKT EMG_REST_HAND_REST P N
XREST REST_NODE N EMG_REST_F1
XHAND HAND_NODE N EMG_HAND_CLOSE_F1
BSELECT P N V={time < 0.5 ? V(REST_NODE,N) : (time < 2.5 ? V(HAND_NODE,N) : V(REST_NODE,N))}
.ENDS EMG_REST_HAND_REST
'''


def load(raw, name):
    lines = (raw / (name + '.hea')).read_text().splitlines()
    fields = lines[0].split()
    nc, fs, count = int(fields[1]), float(fields[2]), int(fields[3])
    assert (nc, fs, count) == (32, 2048.0, 10240), 'Unexpected header'
    a = np.fromfile(raw / (name + '.dat'), dtype='<i2')
    assert a.size == count * nc, 'Record length mismatch'
    a = a.reshape(count, nc)
    labels, volts = [], []
    for i, line in enumerate(lines[1:1+nc]):
        f = line.split()
        assert f[1] == '16', 'Only format 16 is supported'
        m = re.fullmatch(r'([\d.eE+-]+)\((-?\d+)\)/mV', f[2])
        assert m, 'Unexpected units/calibration'
        assert int(a[0, i]) == int(f[5]), 'Initial sample mismatch'
        assert int(a[:, i].astype(np.int64).sum()) % 65536 == int(f[6]) % 65536, 'Checksum mismatch'
        labels.append(f[-1])
        volts.append((a[:, i].astype(float)-int(m[2]))/float(m[1])*1e-3)
    return np.arange(count)/fs, volts[labels.index('F1')]


def pwl(name, t, e):
    lines = [f'.SUBCKT {name} P N', 'VREPLAY P N PWL(']
    lines += [f'+ {s:.12g} {v:.12g}' for s, v in zip(t, 1.650+e)]
    lines += [f'+ 5 {1.650+e[-1]:.12g}', '+ )', f'.ENDS {name}', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--raw-dir', type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    raw = args.raw_dir.resolve() if args.raw_dir else out/'raw'
    raw.mkdir(parents=True, exist_ok=True)
    manifest = {
        'dataset': 'GRABMyo', 'version': '1.1.0', 'license': 'CC BY 4.0',
        'citation': 'Jiang, Pradhan & He (2024), doi:10.13026/89dm-f662',
        'paper': 'Pradhan, He & Jiang (2022), doi:10.1038/s41597-022-01836-y',
        'participant': 1, 'session': 1, 'trial': 1, 'channel': 'F1',
        'processing': 'Header calibration to V; +1.650 V for IN+; no extra filtering, normalization, mean removal or gain-500 division; PWL linear interpolation.',
        'prior_processing': 'Original study describes 10-500 Hz band-pass and 60 Hz notch.',
        'selection': 'REST t<0.5; HAND 0.5<=t<2.5; REST t>=2.5. Original record time is not reset.',
        'files': {}, 'statistics': {},
    }
    chunks = [
        '* GRABMyo v1.1.0 F1 replay; Jiang, Pradhan & He (2024)',
        '* DOI 10.13026/89dm-f662; data CC BY 4.0',
        '* Header-calibrated V + 1.650 V; no added normalization/filtering.',
        '* Not raw electrode/common-mode reconstruction.', '',
    ]
    for label, (name, hea_hash, dat_hash) in RECORDS.items():
        for ext, expected in [('.hea', hea_hash), ('.dat', dat_hash)]:
            p = raw/(name+ext)
            url = BASE+p.name
            if not p.exists():
                with urllib.request.urlopen(url, timeout=60) as response:
                    p.write_bytes(response.read())
            actual = hashlib.sha256(p.read_bytes()).hexdigest()
            assert actual == expected, f'SHA-256 mismatch: {p.name}'
            manifest['files'][p.name] = {'sha256': actual, 'url': url, 'bytes': p.stat().st_size}
        t, e = load(raw, name)
        assert np.isfinite(e).all()
        np.savetxt(out/(label+'_F1.csv'), np.column_stack([t,e,1.650+e]),
                   delimiter=',', header='time_s,emg_V,IN_plus_V', comments='', fmt='%.12g')
        model = 'EMG_REST_F1' if label == 'rest' else 'EMG_HAND_CLOSE_F1'
        source = pwl(model,t,e)
        pairs = np.array([list(map(float,line[2:].split())) for line in source.splitlines() if line.startswith('+ ') and line != '+ )'])
        assert len(pairs) == len(t)+1 and np.all(np.diff(pairs[:,0])>0)
        assert np.max(np.abs(pairs[:-1,1]-(1.650+e))) < 1e-10
        chunks.append(source)
        manifest['statistics'][label] = {
            'samples': len(t), 'fs_hz': 2048, 'mean_uV': float(e.mean()*1e6),
            'rms_uV': float(np.sqrt(np.mean(e**2))*1e6),
            'min_uV': float(e.min()*1e6), 'max_uV': float(e.max()*1e6),
            'mean_abs_uV': float(np.mean(np.abs(e))*1e6),
        }
    chunks.append(COMPOSITE)
    (out/'emg_F1_replay_v2.lib').write_text('\n'.join(chunks))
    (out/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(out),'statistics':manifest['statistics'],
                      'validated':'SHA-256, all-channel WFDB length/initial values/checksums, monotonic PWL times and amplitude round-trip'},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
