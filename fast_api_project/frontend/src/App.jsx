import { useEffect, useState, useCallback } from 'react';
import api from './api/client';
import AddProject from './components/AddProject';
import TaskList from './components/TaskList';
import UsersPage from './pages/UsersPage'; // تأكد من استيراده

function App() {
  const [projects, setProjects] = useState([]);
  const [expandedProjects, setExpandedProjects] = useState([]);
  const [view, setView] = useState('projects'); 

  // 1. تعريف دالة جلب البيانات (مستقرة بفضل useCallback)
  const fetchProjects = useCallback(async () => {
    try {
      const response = await api.get('/projects/');
      setProjects(response.data);
    } catch (error) {
      console.error("خطأ في جلب المشاريع:", error);
    }
  }, []);

  // 2. استخدام useEffect بشكل صحيح وآمن
  useEffect(() => {
    let isMounted = true;

    const loadData = async () => {
      if (isMounted) {
        await fetchProjects();
      }
    };

    loadData();

    return () => {
      isMounted = false;
    };
  }, [fetchProjects]);

  const toggleProjectTasks = (projectId) => {
    setExpandedProjects((prev) =>
      prev.includes(projectId)
        ? prev.filter((id) => id !== projectId)
        : [...prev, projectId]
    );
  };

  const handleNewProject = (newProject) => {
    setProjects((prev) => [...prev, newProject]);
  };

  const deleteProject = async (id) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المشروع؟')) {
      try {
        await api.delete(`/projects/${id}`);
        setProjects((prev) => prev.filter((p) => p.id !== id));
      } catch (error) {
        console.error("خطأ في الحذف:", error);
        alert("فشل الحذف. تأكد من أن المشروع لا يحتوي على مهام");
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4 sm:px-6 lg:px-8" dir="rtl">
      <div className="max-w-4xl mx-auto">
        
        {/* 1. قائمة التنقل العلوي */}
        <nav className="flex justify-center gap-4 mb-10 bg-white p-2 rounded-2xl shadow-sm max-w-fit mx-auto border border-gray-200">
          <button 
            onClick={() => setView('projects')}
            className={`px-8 py-2 rounded-xl font-bold transition-all cursor-pointer ${view === 'projects' ? 'bg-indigo-600 text-white shadow-lg' : 'text-gray-500 hover:bg-gray-50'}`}
          >
            📁 إدارة المشاريع
          </button>
          <button 
            onClick={() => setView('users')}
            className={`px-8 py-2 rounded-xl font-bold transition-all cursor-pointer ${view === 'users' ? 'bg-indigo-600 text-white shadow-lg' : 'text-gray-500 hover:bg-gray-50'}`}
          >
            👥 إدارة المستخدمين
          </button>
        </nav>

        {/* 2. عرض المحتوى بناءً على اختيار المستخدم */}
        {view === 'projects' ? (
          <>
            <header className="mb-10 text-center">
              <h1 className="text-4xl font-extrabold text-indigo-600 mb-2">إدارة المشاريع</h1>
              <p className="text-gray-500">نظام تنظيم الأعمال والمهام</p>
            </header>

            <section className="bg-white shadow-xl rounded-2xl p-6 mb-8 border border-gray-100 transition-all hover:shadow-2xl">
              <AddProject onProjectAdded={handleNewProject} />
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                <span className="bg-indigo-100 text-indigo-600 p-2 rounded-lg ml-3">📂</span>
                المشاريع الحالية ({projects.length})
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {projects.map(project => (
                  <div key={project.id} className="group bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all relative overflow-hidden flex flex-col">
                    <div className="absolute top-0 right-0 w-2 h-full bg-indigo-500"></div>
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-xl font-bold text-gray-800">{project.title}</h3>
                      <button onClick={() => deleteProject(project.id)} className="text-gray-300 hover:text-red-500 transition-colors p-1 text-xl cursor-pointer">🗑️</button>
                    </div>
                    <p className="text-gray-600 text-sm mb-6 flex-grow">{project.description || "لا يوجد وصف"}</p>
                    <button 
                      onClick={() => toggleProjectTasks(project.id)}
                      className="text-sm font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-lg transition-colors border border-indigo-100 mb-4 cursor-pointer"
                    >
                      {expandedProjects.includes(project.id) ? 'إخفاء المهام ↑' : 'عرض المهام ↓'}
                    </button>
                    {expandedProjects.includes(project.id) && <TaskList projectId={project.id} />}
                    <div className="mt-4 pt-4 flex justify-between items-center text-[10px] text-gray-400 border-t border-gray-50">
                      <span>ID: #{project.id}</span>
                      <span className="bg-green-100 text-green-600 px-2 py-0.5 rounded-full font-bold">نشط</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        ) : (
          <UsersPage />
        )}

      </div>
    </div>
  );
}

export default App;