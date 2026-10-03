import { SPEAKERS } from '../../utils/constants.js';

export default function SpeakerSelector({ currentSpeaker, onChange, speakersPresent = [] }) {
  return (
    <div className="speakers" role="radiogroup" aria-label="Who is speaking">
      {speakersPresent.map((s) => (
        <label key={s} className={currentSpeaker === s ? 'seg on' : 'seg'} style={{ '--c': SPEAKERS[s].color }}>
          <input type="radio" name="speaker" checked={currentSpeaker === s} onChange={() => onChange(s)} />
          <i />I am the {SPEAKERS[s].label.toLowerCase()}
        </label>
      ))}
    </div>
  );
}
