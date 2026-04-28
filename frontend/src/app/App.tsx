import { RouterProvider } from 'react-router';
import { router } from './routes';
import { ValidationProvider } from './ValidationContext';

export default function App() {
  return (
    <ValidationProvider>
      <RouterProvider router={router} />
    </ValidationProvider>
  );
}