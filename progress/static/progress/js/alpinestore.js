document.addEventListener('alpine:init', () => {
    Alpine.store('section', {
        
        activeSection: [
            {name:'home', isActive:null},
            {name:'all', isActive:true},
            {name:'public', isActive:null},
            {name:'private', isActive:null},
        ],

        updateActive(sectionName) {
            this.activeSection =  this.activeSection.map(section => ({...section, isActive: section.name == sectionName}))
        },

        isActive(sectionName) {
            return this.activeSection.find((section) => section.name === sectionName).isActive
        }
    
    })
  
  })