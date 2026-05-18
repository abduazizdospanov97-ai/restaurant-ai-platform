import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import { env } from './config/env';
import { errorMiddleware } from './middlewares/error.middleware';
import authRoutes from './modules/auth/auth.routes';
import studentRoutes from './modules/students/students.routes';

const app = express();

app.use(helmet());
app.use(cors({ origin: env.CORS_ORIGIN }));
app.use(express.json());
app.use(morgan('dev'));

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'educrm-api' });
});

app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/students', studentRoutes);

app.get('/api/v1', (_req, res) => {
  res.json({ message: 'EduCRM API started' });
});

app.use(errorMiddleware);

export default app;
