# 🎨 TeleFlow Design System

Современная дизайн-система для TeleFlow Platform, основанная на принципах ясности, продуктивности и эстетической привлекательности.

---

## 📋 Обзор

**Дата редизайна:** 12 марта 2026  
**Версия:** 2.0  
**Стек:** CSS Variables + React Components

---

## 🎯 Принципы дизайна

### 1. Ясность
- Чёткая иерархия контента
- Читаемые шрифты и контраст
- Интуитивно понятные элементы управления

### 2. Продуктивность
- Быстрый доступ к функциям
- Минимизация кликов
- Умные умолчания

### 3. Эстетика
- Современные градиенты
- Плавные анимации
- Согласованность во всём

---

## 🎨 Цветовая палитра

### Primary (Modern Blue)
```
--tf-primary-50:  #eff6ff
--tf-primary-500: #3b82f6
--tf-primary-600: #2563eb  ← Основной
--tf-primary-700: #1d4ed8
```

### Success (Emerald)
```
--tf-success-500: #10b981
--tf-success-600: #059669  ← Основной
--tf-success-700: #047857
```

### Danger (Rose)
```
--tf-danger-500:  #f43f5e
--tf-danger-600:  #e11d48  ← Основной
--tf-danger-700:  #be123c
```

### Warning (Amber)
```
--tf-warning-500: #f59e0b
--tf-warning-600: #d97706  ← Основной
--tf-warning-700: #b45309
```

### Neutral (Slate)
```
--tf-slate-50:  #f8fafc
--tf-slate-100: #f1f5f9
--tf-slate-500: #64748b
--tf-slate-800: #1e293b
--tf-slate-900: #0f172a
```

---

## 📐 Размеры и отступы

### Spacing Scale
```
--tf-spacing-1:  0.25rem  (4px)
--tf-spacing-2:  0.5rem   (8px)
--tf-spacing-3:  0.75rem  (12px)
--tf-spacing-4:  1rem     (16px)
--tf-spacing-5:  1.25rem  (20px)
--tf-spacing-6:  1.5rem   (24px)
--tf-spacing-8:  2rem     (32px)
--tf-spacing-10: 2.5rem   (40px)
--tf-spacing-12: 3rem     (48px)
```

### Border Radius
```
--tf-radius-sm:   0.25rem
--tf-radius-md:   0.375rem
--tf-radius-lg:   0.5rem
--tf-radius-xl:   0.75rem
--tf-radius-2xl:  1rem
--tf-radius-full: 9999px
```

---

## 🔤 Типографика

### Шрифты
```css
--tf-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
--tf-font-mono: 'JetBrains Mono', 'Fira Code', monospace
```

### Размеры шрифтов
```
--tf-font-size-xs:   0.75rem   (12px)
--tf-font-size-sm:   0.875rem  (14px)
--tf-font-size-base: 1rem      (16px)
--tf-font-size-lg:   1.125rem  (18px)
--tf-font-size-xl:   1.25rem   (20px)
--tf-font-size-2xl:  1.5rem    (24px)
--tf-font-size-3xl:  1.875rem  (30px)
```

### Насыщенность
```
--tf-font-weight-normal:   400
--tf-font-weight-medium:   500
--tf-font-weight-semibold: 600
--tf-font-weight-bold:     700
```

---

## 🎭 Компоненты

### Button
```tsx
<Button variant="primary" size="md">
  Click me
</Button>

// Variants: primary, secondary, success, danger, warning, outline, ghost
// Sizes: xs, sm, md, lg, xl
```

### Card
```tsx
<Card title="Card Title" subtitle="Optional subtitle">
  Card content goes here
</Card>
```

### Badge
```tsx
<Badge variant="primary">New</Badge>

// Variants: primary, success, danger, warning, secondary
```

### Modal
```tsx
<Modal isOpen={true} onClose={() => setIsOpen(false)} title="Modal Title">
  Content
</Modal>
```

---

## 🎬 Анимации

### Transitions
```css
--tf-transition-fast:   150ms cubic-bezier(0.4, 0, 0.2, 1)
--tf-transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1)
--tf-transition-slow:   350ms cubic-bezier(0.4, 0, 0.2, 1)
```

### Shadows (при наведении)
```css
--tf-shadow-sm:  0 1px 3px 0 rgba(15, 23, 42, 0.1)
--tf-shadow-md:  0 4px 6px -1px rgba(15, 23, 42, 0.1)
--tf-shadow-lg:  0 10px 15px -3px rgba(15, 23, 42, 0.1)
```

---

## 📱 Адаптивность

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Mobile-first подход
Все компоненты сначала проектируются для мобильных, затем масштабируются для десктопа.

---

## 🚀 Использование

### 1. Импорт стилей
```tsx
import './index.css'  // Главный файл с импортами
```

### 2. Использование компонентов
```tsx
import { Button, Card, Badge } from '@/components/ui'

function MyComponent() {
  return (
    <Card title="Example">
      <Button variant="primary">Action</Button>
      <Badge variant="success">Active</Badge>
    </Card>
  )
}
```

### 3. Кастомизация через CSS Variables
```css
.my-component {
  background: var(--tf-bg-primary);
  color: var(--tf-text-primary);
  padding: var(--tf-spacing-4);
  border-radius: var(--tf-radius-lg);
}
```

---

## 📊 Примеры UI паттернов

### Dashboard Layout
```
┌────────────────────────────────────────────┐
│ Sidebar (280px)     │ Main Content         │
│ ────────────────────│ ──────────────────── │
│ ⚡ TeleFlow         │ Header (sticky)      │
│                     │ ──────────────────── │
│ 📊 Dashboard        │ Page Content         │
│ 📰 Content          │                      │
│ 📤 Publishing       │                      │
│ 🎯 Funnels          │                      │
│ 🤖 Userbot          │                      │
│ 📈 Promotion        │                      │
│ 📉 Analytics        │                      │
│ ⚙️ Settings         │                      │
│                     │                      │
│ ────────────────────│                      │
│ 👤 User Info        │                      │
└────────────────────────────────────────────┘
```

### Card Grid
```tsx
<div className="d-flex flex-wrap gap-4">
  <Card style={{ flex: '1 1 300px' }}>Card 1</Card>
  <Card style={{ flex: '1 1 300px' }}>Card 2</Card>
  <Card style={{ flex: '1 1 300px' }}>Card 3</Card>
</div>
```

---

## 🎯 Best Practices

### ✅ Делайте
- Используйте семантические названия вариантов
- Следуйте иерархии размеров
- Добавляйте hover/focus состояния
- Тестируйте на контрастность

### ❌ Не делайте
- Не создавайте новые цвета без необходимости
- Не игнорируйте accessibility
- Не используйте inline стили для layout
- Не забывайте про focus states

---

## 🔧 Разработка новых компонентов

1. Создайте `.tsx` файл компонента
2. Создайте `.css` файл со стилями
3. Добавьте CSS variables вместо хардкода
4. Экспортируйте из `index.ts`
5. Протестируйте на разных размерах экрана

---

## 📝 Changelog

### v2.0 (12 марта 2026)
- ✨ Полная переработка дизайн-системы
- 🎨 Современные градиенты и тени
- 📱 Улучшенная адаптивность
- ⚡ Плавные анимации
- 🎯 Новый Dashboard Layout
- 🔘 Обновлённые Button, Card, Badge

### v1.0 (Initial)
- Базовые компоненты на Bootstrap

---

*Design System maintained by TeleFlow Team*
