import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../../lib/prisma';

const router = Router();

const studentSchema = z.object({
  fullName: z.string().min(2),
  phone: z.string().optional(),
  status: z.enum(['ACTIVE', 'INACTIVE']).optional()
});

router.get('/', async (req, res, next) => {
  try {
    const search = (req.query.search as string | undefined)?.trim();
    const page = Number(req.query.page ?? 1);
    const limit = Number(req.query.limit ?? 10);
    const skip = (page - 1) * limit;
    const where = search ? { fullName: { contains: search, mode: 'insensitive' as const } } : {};
    const [items, total] = await Promise.all([
      prisma.student.findMany({ where, skip, take: limit, orderBy: { createdAt: 'desc' } }),
      prisma.student.count({ where })
    ]);
    res.json({ items, page, limit, total, totalPages: Math.ceil(total / limit) });
  } catch (error) {
    next(error);
  }
});

router.post('/', async (req, res, next) => {
  try {
    const body = studentSchema.parse(req.body);
    const student = await prisma.student.create({ data: body });
    res.status(201).json(student);
  } catch (error) {
    next(error);
  }
});

router.patch('/:id', async (req, res, next) => {
  try {
    const body = studentSchema.partial().parse(req.body);
    const student = await prisma.student.update({ where: { id: req.params.id }, data: body });
    res.json(student);
  } catch (error) {
    next(error);
  }
});

router.delete('/:id', async (req, res, next) => {
  try {
    await prisma.student.delete({ where: { id: req.params.id } });
    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

export default router;
