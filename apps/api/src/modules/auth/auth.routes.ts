import { Router } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import { env } from '../../config/env';
import { prisma } from '../../lib/prisma';

const router = Router();

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6)
});

router.post('/register', async (req, res, next) => {
  try {
    const body = loginSchema.extend({ fullName: z.string().min(2), role: z.enum(['ADMIN', 'TEACHER', 'CASHIER']).optional() }).parse(req.body);
    const passwordHash = await bcrypt.hash(body.password, 10);
    const user = await prisma.user.create({
      data: { fullName: body.fullName, email: body.email, passwordHash, role: body.role ?? 'TEACHER' },
      select: { id: true, fullName: true, email: true, role: true }
    });
    res.status(201).json(user);
  } catch (error) {
    next(error);
  }
});

router.post('/login', async (req, res, next) => {
  try {
    const body = loginSchema.parse(req.body);
    const user = await prisma.user.findUnique({ where: { email: body.email } });
    if (!user) return res.status(401).json({ message: 'Invalid credentials' });
    const ok = await bcrypt.compare(body.password, user.passwordHash);
    if (!ok) return res.status(401).json({ message: 'Invalid credentials' });
    const token = jwt.sign({ sub: user.id, role: user.role, email: user.email }, env.JWT_SECRET, { expiresIn: '1d' });
    res.json({ token, user: { id: user.id, fullName: user.fullName, email: user.email, role: user.role } });
  } catch (error) {
    next(error);
  }
});

export default router;
