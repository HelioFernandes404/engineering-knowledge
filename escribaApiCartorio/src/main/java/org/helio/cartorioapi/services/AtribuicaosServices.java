package org.helio.cartorioapi.services;

import org.helio.cartorioapi.dto.AtribuicaosDTO;
import org.helio.cartorioapi.dto.AtribuicaosMinDTO;
import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.repositorios.AtribuicaoRepository;
import org.helio.cartorioapi.services.exceptions.DatabaseException;
import org.helio.cartorioapi.services.exceptions.ResourceNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class AtribuicaosServices {
    
    @Autowired
    private AtribuicaoRepository repository;

    @Transactional(readOnly = true)
    public Page<AtribuicaosMinDTO> findAll(Pageable pageable) {
        Page<Atribuicaos> result = repository.findAllBy(pageable);
        return result.map(x -> new AtribuicaosMinDTO(x));
    }

    @Transactional(readOnly = true)
    public AtribuicaosDTO findById(String id) {
        Atribuicaos entity = repository.findById(id).orElseThrow(
                () -> new ResourceNotFoundException("Recurso não encontrado"));
        return new AtribuicaosDTO(entity);
    }

    @Transactional
    public AtribuicaosDTO insert(AtribuicaosDTO dto) {

        Optional<Atribuicaos> existingById = repository.findById(dto.getId());
        if (existingById.isPresent()) {
            throw new DatabaseException("Registro já cadastrado");
        }

        Optional<Atribuicaos> existingByNome = repository.findByNome(dto.getNome());
        if (existingByNome.isPresent()) {
            throw new DatabaseException("Nome já informado no registro com código: " + existingByNome.get().getId());
        }

        Atribuicaos entity = new Atribuicaos(dto);
        Atribuicaos savedEntity = repository.save(entity);
        return new AtribuicaosDTO(savedEntity);
    }

    @Transactional
    public AtribuicaosDTO update(String id, AtribuicaosDTO dto) {
        Optional<Atribuicaos> existing = repository.findById(id);
        if (!existing.isPresent()) {
            throw new DatabaseException("Registro com ID " + id + " não encontrado");
        }
        Atribuicaos entity = existing.get();
        if (!entity.getNome().equals(dto.getNome())) {
            Optional<Atribuicaos> duplicate = repository.findByNome(dto.getNome());
            if (duplicate.isPresent()) {
                throw new DatabaseException("Nome já informado no registro com código " + duplicate.get().getId());
            }
        }
        entity.setNome(dto.getNome());
        entity.setSituacao(dto.isSituacao());
        Atribuicaos savedEntity = repository.save(entity);
        return new AtribuicaosDTO(savedEntity);
    }

    @Transactional(propagation = Propagation.SUPPORTS)
    public void delete(String id) {
        try {
            repository.deleteById(id);
        } catch (EmptyResultDataAccessException e) {
            throw new ResourceNotFoundException("Recurso não encontrado");
        } catch (DataIntegrityViolationException e) {
            throw new DatabaseException("Registro utilizado em outro cadastro");
        }
    }

    private Atribuicaos copyDtoToEntity(AtribuicaosDTO dto) {
        Atribuicaos entity = new Atribuicaos();
        entity.setId(dto.getId());
        entity.setNome(dto.getNome());
        entity.setSituacao(dto.isSituacao());

        return entity;
    }

}
