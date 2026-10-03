import { useState } from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, Users, UserCog, BarChart3 } from 'lucide-react';
import { LANGUAGES, T, getLang } from '../utils/constants.js';

export default function Landing() {
  const [lang, setLang] = useState(getLang());
  const pick = (c) => { localStorage.setItem('lang', c); setLang(c); };
  const tr = T[lang];
  const roles = [
    [GraduationCap, 'Learner', '/setup'], [Users, 'Parent', '/setup'],
    [UserCog, 'Counsellor', '/counsellor'], [BarChart3, 'Admin', '/admin'],
  ];
  return (
    <div className="landing">
      <section className="hero">
        <h1>{tr.title}</h1>
        <p className="lead">{tr.sub}</p>
        <div className="lang-row" role="radiogroup" aria-label="Language">
          {Object.values(LANGUAGES).map((l) => (
            <button key={l.code} role="radio" aria-checked={lang === l.code} className={lang === l.code ? 'lang on' : 'lang'} onClick={() => pick(l.code)}>{l.name}</button>
          ))}
        </div>
        <Link to="/setup" className="btn big">{tr.start}</Link>
      </section>
      <section className="roles" aria-label="Who is this for">
        {roles.map(([Icon, label, to]) => (
          <Link key={label} to={to} className="role"><Icon size={28} aria-hidden /><span>{label}</span></Link>
        ))}
      </section>
      <footer className="footer">Ministry of Skill Development and Entrepreneurship · Vocational Education Family Decision-Support</footer>
    </div>
  );
}
