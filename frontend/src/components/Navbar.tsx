import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  const linkClass = (path: string) =>
    `rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
      location.pathname === path
        ? 'bg-indigo-100 text-indigo-700'
        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
    }`;

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="text-xl font-bold text-indigo-600">
            Chron-Track
          </Link>
          <div className="flex items-center gap-1">
            <Link to="/" className={linkClass('/')}>
              Courses
            </Link>
            <Link to="/records" className={linkClass('/records')}>
              Records
            </Link>
          </div>
        </div>

        {user && (
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">{user.username}</span>
            <button
              onClick={handleLogout}
              className="rounded-lg px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-900"
            >
              Deconnexion
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
