import { useState } from 'react';
import api from '../api/client';

const AddProject = ({ onProjectAdded }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [ownerId] = useState(1); // للمستخدم الافتراضي رقم 1

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/projects/', {
        title: title,
        description: description,
        owner_id: ownerId
      });
      
      setTitle('');
      setDescription('');
      if (onProjectAdded) onProjectAdded(response.data);
      
    } catch (error) {
      console.error("خطأ:", error);
      alert('فشل الاتصال بالخادم. تأكد من تشغيل FastAPI');
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
        <span className="text-indigo-500 text-2xl">+</span>
        إضافة مشروع جديد
      </h3>
      
      <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">عنوان المشروع</label>
          <input 
            type="text" 
            placeholder="مثلاً: تطبيق إدارة المهام" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            required 
            className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all placeholder:text-gray-400"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">الوصف</label>
          <textarea 
            placeholder="اكتب تفاصيل المشروع هنا..." 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
            rows="3"
            className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all placeholder:text-gray-400 resize-none"
          />
        </div>

        <button 
          type="submit" 
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-indigo-200 transition-all active:scale-95 flex items-center justify-center gap-2"
        >
          <span>🚀</span>
          حفظ المشروع
        </button>
      </form>
    </div>
  );
};

export default AddProject;