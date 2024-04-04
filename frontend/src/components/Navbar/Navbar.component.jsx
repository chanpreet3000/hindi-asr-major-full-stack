import './Navbar.styles.css';
const Navbar = () => {
  return (
    <nav className="main-nav">
      <div className="main-nav__items">
        <div className="main-nav__brand">
          <a href="/">Major Project</a>
        </div>
        <div className="main-nav__links">
          <a className="main-nav__link developers" href="#main-footer">
            Developers
          </a>
        </div>
      </div>
    </nav>
  );
};
export default Navbar;
