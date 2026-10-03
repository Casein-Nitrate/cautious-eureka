import { NavLink, Link } from 'react-router-dom';

export default function Header() {
  const cls = ({ isActive }) => (isActive ? 'nav-link active' : 'nav-link');
  return (
    <header className="header">
      <Link to="/" className="brand" aria-label="VocEd home"><span className="brand-mark">V</span>VocEd Counselling</Link>
      <nav aria-label="Main">
        <NavLink to="/setup" className={cls}>Families</NavLink>
        <NavLink to="/counsellor" className={cls}>Counsellor</NavLink>
        <NavLink to="/admin" className={cls}>Admin</NavLink>
      </nav>
    </header>
  );
}
