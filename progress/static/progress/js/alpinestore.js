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
        },
        deactivate() {
            this.activeSection = this.activeSection.map(section => ({...section, isActive: false}))
        }
    
    }),

    Alpine.store('notes', {
        editProccess(noteId, noteMessage) {
            Array.from(document.getElementsByClassName('form-edit-notes')).forEach(form => {
                
                // update form data
                form.note.value = noteMessage;
                form.noteId.value = noteId;

                // const pattern = /\/\d+\//;
                // const url = form.action
                // const newUrl = url.replace(pattern, `/${noteId}/`)
                // const HTMXheaders = form.getAttribute('hx-headers')

                // form.addEventListener('htmx:beforeRequest', function Stop(e) {
                //     e.preventDefault()
                //     e.target.removeEventListener('htmx:beforeRequest', Stop) 

                //     htmx.ajax('PUT', `${newUrl}`, {source: e.target})
                //     // console.log(form)
                //     // const newForm = new FormData(form)
                //     // fetch(newUrl, {
                //     //     method: 'PUT',
                //     //     body: newForm,
                //     //     headers: {
                //     //         HTMXheaders
                //     //       },
                //     // })
                // })

               
            })
            
        }
        
    
    })
  })


document.addEventListener("htmx:confirm", function(e) {
    // if deleting a note
    if (Array.from(e.target.classList).includes('delete-note'))  { 
        e.preventDefault()
  
      // Mostrar un cuadro de diálogo personalizado con Swal
      Swal.fire({
        title: "Proceed?",
        text: `I ask you... ${e.detail.question}`
      }).then(function(result) {
        if (result.isConfirmed) {
            const event = new CustomEvent("delete-note");
            e.target.dispatchEvent(event)
            e.detail.issueRequest(true); // this continue the request

            // const event = new CustomEvent("deleterow", {detail : {itemId : e.target.dataset.rowid}});
            // window.dispatchEvent(event);

        } 
      });
    }
  });

// https://www.reddit.com/r/htmx/comments/10hu6wp/how_to_know_which_event_was_triggered/
htmx.on("htmx:afterRequest", (e) => {
// if creating a Note 
if (Array.from(e.target.classList).includes("form-notes")) {
    if (e.detail.successful) {
        e.target.note.value = ''
        const event = new CustomEvent("upp-note-counter");
        e.target.dispatchEvent(event)

        Swal.fire({
            icon: "success",
            title: "Note Created",
            showConfirmButton: false,
            timer: 1500
          });

    } else {

        console.log(e)
        console.log(e.target)

        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: e.detail.xhr.responseText,
            showConfirmButton: false,
            timer: 2500
          });

    }
} 
// if editing a Note
else if (Array.from(e.target.classList).includes("form-edit-notes")) {
    if (e.detail.successful) {
        e.target.note.value = ''
        const event = new CustomEvent("set-editing-false");
        e.target.dispatchEvent(event)

        Swal.fire({
            icon: "success",
            title: "Note Updated",
            showConfirmButton: false,
            timer: 1500
          });

    } else {

        console.log(e)
        console.log(e.target)

        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: e.detail.xhr.responseText,
            showConfirmButton: false,
            timer: 2500
          });

    }
} 

});