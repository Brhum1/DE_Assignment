import { useState, useEffect, useCallback } from 'react';
import api from '../api/client';

const TaskList = ({ projectId }) => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');

  // 1. تعريف الدالة باستخدام useCallback لضمان استقرارها
  const fetchTasks = useCallback(async () => {
    try {
      const res = await api.get(`/tasks/project/${projectId}`);
      // تحديث الحالة
      setTasks(res.data);
    } catch (err) {
      console.error("خطأ في جلب المهام", err);
    }
  }, [projectId]);

  // 2. الحل الجذري: تشغيل الدالة بشكل غير متزامن داخل الـ Effect
  useEffect(() => {
    let isMounted = true;

    const loadTasks = async () => {
      if (isMounted) {
        await fetchTasks();
      }
    };

    loadTasks();

    // دالة تنظيف لمنع تحديث الحالة إذا أغلق المكون
    return () => {
      isMounted = false;
    };
  }, [fetchTasks]);

  // 3. إضافة مهمة جديدة
  const addTask = async (e) => {
    if (e.key === 'Enter' && newTask.trim()) {
      try {
        const res = await api.post('/tasks/', { 
          title: newTask, 
          project_id: projectId,
          is_completed: false 
        });
        setTasks((prev) => [...prev, res.data]);
        setNewTask('');
      } catch (err) {
        console.error("خطأ في الإضافة", err);
      }
    }
  };

  const toggleTask = async (task) => {
    try {
      const res = await api.patch(`/tasks/${task.id}`, { 
        is_completed: !task.is_completed 
      });
      setTasks(prev => prev.map(t => t.id === task.id ? res.data : t));
    } catch (err) {
      console.error("خطأ في التحديث", err);
    }
  };

  const deleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      setTasks(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      console.error("خطأ في الحذف", err);
    }
  };

  return (
    <div className="mt-4 space-y-3 bg-gray-50 p-4 rounded-xl border border-gray-100" dir="rtl">
      <div className="flex items-center gap-2 bg-white p-2 rounded-lg shadow-sm border border-gray-200 focus-within:ring-2 focus-within:ring-indigo-200 transition-all">
        <span className="text-gray-400">📝</span>
        <input 
          type="text" 
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          onKeyDown={addTask}
          placeholder="أضف مهمة واضغط Enter..."
          className="flex-1 bg-transparent outline-none text-sm placeholder:text-gray-400 text-right"
        />
      </div>

      <div className="space-y-2 max-h-48 overflow-y-auto pr-1 text-right">
        {tasks.length > 0 ? (
          tasks.map(task => (
            <div key={task.id} className="flex items-center justify-between group bg-white p-2 rounded-lg border border-transparent hover:border-indigo-100 transition-all shadow-sm">
              <div className="flex items-center gap-3">
                <input 
                  type="checkbox" 
                  checked={task.is_completed} 
                  onChange={() => toggleTask(task)}
                  className="w-4 h-4 rounded text-indigo-600 cursor-pointer"
                />
                <span className={`text-sm ${task.is_completed ? 'line-through text-gray-400' : 'text-gray-700 font-medium'}`}>
                  {task.title}
                </span>
              </div>
              <button 
                onClick={() => deleteTask(task.id)}
                className="opacity-0 group-hover:opacity-100 text-gray-300 hover:text-red-500 transition-all text-xs p-1"
              >
                ✕
              </button>
            </div>
          ))
        ) : (
          <p className="text-center text-[10px] text-gray-400 py-2">لا توجد مهام</p>
        )}
      </div>
    </div>
  );
};

export default TaskList;